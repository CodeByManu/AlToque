import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/tables", tags=["tables"])


@router.get("", response_model=list[schemas.TableOut])
def list_tables(
    restaurant_id: uuid.UUID, db: Session = Depends(get_db)
) -> list[models.Table]:
    rows = list(
        db.execute(
            select(models.Table)
            .where(models.Table.restaurant_id == restaurant_id)
            .where(models.Table.active.is_(True))
            .order_by(models.Table.number)
        ).scalars()
    )
    if not rows:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encontraron mesas activas para este restaurante",
        )
    logger.info("listando %d mesas para restaurante %s", len(rows), restaurant_id)
    return rows
