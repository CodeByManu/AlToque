import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from twilio.base.exceptions import TwilioRestException

from app import models, schemas
from app.db import get_db
from app.services.whatsapp import TwilioNotConfigured, send_test_message

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])


_SEED_RESTAURANT_NAME = "Tiramisú"
_SEED_WAITERS = ["Pedro", "Ana", "Luis"]
_SEED_TABLE_NUMBERS = [1, 2, 3, 4, 5]
_SEED_QUESTIONS = [
    ("¿Cómo estuvo la comida?", "comida"),
    ("¿Qué tal el servicio del garzón?", "servicio"),
    ("¿Cómo fue el tiempo de espera?", "espera"),
    ("¿Te gustó el ambiente?", "ambiente"),
    ("¿Volverías?", "general"),
]


@router.post(
    "/seed",
    response_model=schemas.SeedOut,
    status_code=status.HTTP_201_CREATED,
)
def seed_database(db: Session = Depends(get_db)) -> schemas.SeedOut:
    # Solo si la BD esta vacia (SPEC §3 admin)
    existing = db.execute(select(func.count(models.Restaurant.id))).scalar_one()
    if existing > 0:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="La base de datos ya tiene datos. Seed solo se ejecuta vacia.",
        )

    restaurant = models.Restaurant(name=_SEED_RESTAURANT_NAME)
    db.add(restaurant)
    db.flush()

    for name in _SEED_WAITERS:
        db.add(models.Waiter(restaurant_id=restaurant.id, name=name, active=True))

    for number in _SEED_TABLE_NUMBERS:
        db.add(models.Table(restaurant_id=restaurant.id, number=number, active=True))

    for text, category in _SEED_QUESTIONS:
        db.add(
            models.Question(
                restaurant_id=restaurant.id,
                text=text,
                category=category,
                active=True,
            )
        )

    db.commit()
    logger.info("seed completado: restaurant_id=%s", restaurant.id)

    return schemas.SeedOut(
        restaurant_id=restaurant.id,
        waiters=len(_SEED_WAITERS),
        tables=len(_SEED_TABLE_NUMBERS),
        questions=len(_SEED_QUESTIONS),
    )


@router.post("/test-whatsapp")
def test_whatsapp() -> dict[str, str]:
    try:
        return send_test_message()
    except TwilioNotConfigured as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(e),
        )
    except TwilioRestException as e:
        logger.error("test-whatsapp fallo en Twilio: %s", e)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Twilio rechazó el envío: {e.msg}",
        )
