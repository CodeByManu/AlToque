import logging
import uuid

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/restaurants", tags=["restaurants"])


@router.get("", response_model=list[schemas.RestaurantOut])
def list_restaurants(db: Session = Depends(get_db)) -> list[models.Restaurant]:
    return list(
        db.execute(select(models.Restaurant).order_by(models.Restaurant.name)).scalars()
    )


@router.get("/{restaurant_id}", response_model=schemas.RestaurantOut)
def get_restaurant(
    restaurant_id: uuid.UUID, db: Session = Depends(get_db)
) -> models.Restaurant:
    restaurant = db.get(models.Restaurant, restaurant_id)
    if restaurant is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Restaurante no encontrado",
        )
    return restaurant
