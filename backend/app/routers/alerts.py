import logging
import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db
from app.ws import broadcast_event

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/alerts", tags=["alerts"])


@router.patch("/{alert_id}/resolve", response_model=schemas.AlertOut)
def resolve_alert(
    alert_id: uuid.UUID,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
) -> schemas.AlertOut:
    alert = db.get(models.Alert, alert_id)
    if alert is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerta no encontrada",
        )
    if alert.resolved_at is not None:
        # Idempotente: si ya estaba resuelta devolvemos lo que hay sin tocar.
        logger.info("resolve_alert: %s ya estaba resuelta, no-op", alert_id)
        return schemas.AlertOut.model_validate(alert)

    alert.resolved_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(alert)

    logger.info("resolve_alert: %s marcada resuelta", alert_id)

    background_tasks.add_task(
        broadcast_event,
        str(alert.restaurant_id),
        {
            "type": "alert_resolved",
            "data": {"id": str(alert.id)},
        },
    )

    return schemas.AlertOut.model_validate(alert)
