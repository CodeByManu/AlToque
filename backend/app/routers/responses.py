import logging

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.services.whatsapp import send_alert
from app.ws import broadcast_event

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/responses", tags=["responses"])

_ALERT_THRESHOLD = 2


@router.post(
    "",
    response_model=schemas.ResponseOut,
    status_code=status.HTTP_201_CREATED,
)
def create_response(
    payload: schemas.ResponseCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> models.Response:
    session_row = db.get(models.SessionRow, payload.session_id)
    if session_row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="session_id no encontrado",
        )

    if payload.action == "answered":
        if payload.rating is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="rating es obligatorio cuando action=answered",
            )
        if payload.question_id is None or payload.question_id != session_row.question_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="question_id no coincide con la pregunta de la sesión",
            )
        question_id_to_store = session_row.question_id
        rating_to_store = payload.rating
    else:  # skipped
        question_id_to_store = None
        rating_to_store = None

    interaction_ms = max(
        int((payload.responded_at - payload.shown_at).total_seconds() * 1000),
        0,
    )

    response = models.Response(
        restaurant_id=session_row.restaurant_id,
        table_id=session_row.table_id,
        waiter_id=session_row.waiter_id,
        question_id=question_id_to_store,
        rating=rating_to_store,
        action=payload.action,
        shown_at=payload.shown_at,
        responded_at=payload.responded_at,
        interaction_ms=interaction_ms,
    )
    db.add(response)
    db.commit()
    db.refresh(response)

    logger.info(
        "response creada %s · action=%s rating=%s interaction_ms=%d",
        response.id,
        response.action,
        response.rating,
        response.interaction_ms,
    )

    # Emision WS para el dashboard
    background_tasks.add_task(
        broadcast_event,
        str(response.restaurant_id),
        {
            "type": "new_response",
            "data": {
                "id": str(response.id),
                "rating": response.rating,
                "action": response.action,
                "interaction_ms": response.interaction_ms,
                "responded_at": response.responded_at.isoformat(),
            },
        },
    )

    # Alerta WhatsApp si rating bajo. El broadcast del 'new_alert' lo emite
    # send_alert() despues de crear el row, asi el dashboard no encuentra la
    # alerta vacia al refetchear.
    if (
        response.action == "answered"
        and response.rating is not None
        and response.rating <= _ALERT_THRESHOLD
    ):
        logger.info(
            "rating %d <= %d, encolando alerta para response %s",
            response.rating,
            _ALERT_THRESHOLD,
            response.id,
        )
        background_tasks.add_task(send_alert, response.id)

    return response
