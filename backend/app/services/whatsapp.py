"""
Envio de alerta WhatsApp cuando un rating es <=2.

Disenado para correr en FastAPI BackgroundTasks: no async, no Celery.
Si Twilio falla o no esta configurado: registramos whatsapp_status='failed'
y NO rompemos el flujo (SPEC §6).
"""
import logging
import uuid
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import select
from sqlalchemy.orm import Session
from twilio.base.exceptions import TwilioRestException
from twilio.rest import Client

from app import config, models
from app.db import SessionLocal
from app.ws import broadcast_event

logger = logging.getLogger(__name__)

_TZ_SANTIAGO = ZoneInfo("America/Santiago")

_TEST_BODY = "AlToque test ✅ — si recibís esto, Twilio está OK."


class TwilioNotConfigured(Exception):
    """Faltan variables de entorno de Twilio."""


def send_test_message() -> dict[str, str]:
    """
    Envia un mensaje de prueba fijo al numero MANAGER_WHATSAPP_TO.
    No toca la tabla alerts: es un test de conectividad puro.

    Levanta TwilioNotConfigured si faltan envs.
    Propaga TwilioRestException si la API rechaza el envio.
    """
    if not config.twilio_configured():
        raise TwilioNotConfigured(
            "Faltan TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, "
            "TWILIO_WHATSAPP_FROM o MANAGER_WHATSAPP_TO en .env"
        )

    client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        from_=config.TWILIO_WHATSAPP_FROM,
        to=config.MANAGER_WHATSAPP_TO,
        body=_TEST_BODY,
    )
    logger.info(
        "test-whatsapp enviado sid=%s status=%s to=%s",
        message.sid,
        message.status,
        config.MANAGER_WHATSAPP_TO,
    )
    return {
        "sid": message.sid,
        "status": message.status,
        "to": config.MANAGER_WHATSAPP_TO,
        "from": config.TWILIO_WHATSAPP_FROM,
        "body": _TEST_BODY,
    }


def _format_message(
    restaurant_name: str,
    table_number: int,
    waiter_name: str,
    question_text: str,
    rating: int,
    responded_at: datetime,
) -> str:
    hora_local = responded_at.astimezone(_TZ_SANTIAGO).strftime("%H:%M")
    return (
        f"🚨 *Alerta AlToque — {restaurant_name}*\n"
        f"\n"
        f"Rating: *{rating}/5*  ·  {hora_local} hrs\n"
        f"Mesa *{table_number}*  ·  Garzón: {waiter_name}\n"
        f"\n"
        f'_"{question_text}"_'
    )


def send_alert(response_id: uuid.UUID) -> None:
    """
    Punto de entrada para FastAPI BackgroundTasks.

    Recibe el response_id y se encarga de:
      1. Abrir su propia sesion de BD (la del request ya esta cerrada).
      2. Crear el row en alerts con status='pending'.
      3. Resolver contexto (restaurant_name, table_number, waiter_name,
         question_text) con un select() plano.
      4. Llamar a Twilio si esta configurado.
      5. Actualizar alerts con 'sent' o 'failed'.
    """
    db: Session = SessionLocal()
    alert: models.Alert | None = None
    try:
        response = db.get(models.Response, response_id)
        if response is None:
            logger.error("send_alert: response %s no encontrado", response_id)
            return

        alert = models.Alert(
            response_id=response.id,
            restaurant_id=response.restaurant_id,
            whatsapp_status="pending",
        )
        db.add(alert)
        db.commit()
        db.refresh(alert)

        # Avisar al dashboard ahora que la fila existe (asi el refetch la ve).
        broadcast_event(
            str(response.restaurant_id),
            {
                "type": "new_alert",
                "data": {
                    "id": str(alert.id),
                    "response_id": str(response.id),
                    "rating": response.rating,
                },
            },
        )

        ctx_stmt = (
            select(
                models.Restaurant.name,
                models.Table.number,
                models.Waiter.name,
                models.Question.text,
            )
            .join(models.Table, models.Table.id == response.table_id)
            .join(models.Waiter, models.Waiter.id == response.waiter_id)
            .join(models.Question, models.Question.id == response.question_id)
            .where(models.Restaurant.id == response.restaurant_id)
        )
        row = db.execute(ctx_stmt).first()
        if row is None:
            logger.error(
                "send_alert: no se pudo resolver contexto para response %s",
                response_id,
            )
            alert.whatsapp_status = "failed"
            db.commit()
            return

        restaurant_name, table_number, waiter_name, question_text = row

        if not config.twilio_configured():
            logger.warning(
                "send_alert: Twilio no configurado, marcando alert %s como failed",
                alert.id,
            )
            alert.whatsapp_status = "failed"
            db.commit()
            return

        body = _format_message(
            restaurant_name=restaurant_name,
            table_number=table_number,
            waiter_name=waiter_name,
            question_text=question_text,
            rating=response.rating,
            responded_at=response.responded_at,
        )

        try:
            client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            message = client.messages.create(
                from_=config.TWILIO_WHATSAPP_FROM,
                to=config.MANAGER_WHATSAPP_TO,
                body=body,
            )
            alert.whatsapp_status = "sent"
            alert.whatsapp_message_sid = message.sid
            alert.sent_at = datetime.now(timezone.utc)
            db.commit()
            logger.info(
                "send_alert: alerta %s enviada (sid=%s)", alert.id, message.sid
            )
        except TwilioRestException as e:
            logger.error("send_alert: Twilio fallo para alert %s: %s", alert.id, e)
            alert.whatsapp_status = "failed"
            db.commit()
    finally:
        db.close()
