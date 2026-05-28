import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/waiters", tags=["waiters"])


@router.get("", response_model=list[schemas.WaiterOut])
def list_waiters(
    restaurant_id: uuid.UUID, db: Session = Depends(get_db)
) -> list[models.Waiter]:
    rows = list(
        db.execute(
            select(models.Waiter)
            .where(models.Waiter.restaurant_id == restaurant_id)
            .where(models.Waiter.active.is_(True))
            .order_by(models.Waiter.name)
        ).scalars()
    )
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron garzones activos para este restaurante",
        )
    logger.info("listando %d garzones para restaurante %s", len(rows), restaurant_id)
    return rows
