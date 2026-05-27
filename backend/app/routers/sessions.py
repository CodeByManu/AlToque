import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.services.questions import pick_question

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sessions", tags=["sessions"])


@router.get("/start", response_model=schemas.SessionStartOut)
def start_session(
    restaurant_id: uuid.UUID = Query(...),
    table_id: uuid.UUID = Query(...),
    waiter_id: uuid.UUID = Query(...),
    db: Session = Depends(get_db),
) -> schemas.SessionStartOut:
    # Validacion: mesa y garzon pertenecen al restaurante y estan activos.
    table = db.execute(
        select(models.Table).where(
            models.Table.id == table_id,
            models.Table.restaurant_id == restaurant_id,
        )
    ).scalar_one_or_none()
    if table is None or not table.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Mesa no encontrada o inactiva para este restaurante",
        )

    waiter = db.execute(
        select(models.Waiter).where(
            models.Waiter.id == waiter_id,
            models.Waiter.restaurant_id == restaurant_id,
        )
    ).scalar_one_or_none()
    if waiter is None or not waiter.active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Garzón no encontrado o inactivo para este restaurante",
        )

    question = pick_question(db, restaurant_id)
    if question is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No hay preguntas activas para este restaurante",
        )

    shown_at = datetime.now(timezone.utc)
    session_row = models.SessionRow(
        restaurant_id=restaurant_id,
        table_id=table_id,
        waiter_id=waiter_id,
        question_id=question.id,
        shown_at=shown_at,
    )
    db.add(session_row)
    db.commit()
    db.refresh(session_row)

    logger.info(
        "session creada %s · mesa=%s garzon=%s pregunta=%s",
        session_row.id,
        table.number,
        waiter.name,
        question.id,
    )

    return schemas.SessionStartOut(
        session_id=session_row.id,
        question=schemas.QuestionOut.model_validate(question),
        shown_at=shown_at,
    )
