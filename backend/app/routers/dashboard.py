import logging
import uuid
from datetime import datetime, timedelta, timezone

from fastapi import APIRouter, Depends, Query
from sqlalchemy import and_, func, select
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/dashboard", tags=["dashboard"])


def _time_window_clause(from_: datetime | None, to_: datetime | None):
    clauses = []
    if from_ is not None:
        clauses.append(models.Response.created_at >= from_)
    if to_ is not None:
        clauses.append(models.Response.created_at <= to_)
    return and_(*clauses) if clauses else None


@router.get("/metrics", response_model=schemas.DashboardMetricsOut)
def metrics(
    restaurant_id: uuid.UUID = Query(...),
    from_: datetime | None = Query(default=None, alias="from"),
    to_: datetime | None = Query(default=None, alias="to"),
    db: Session = Depends(get_db),
) -> schemas.DashboardMetricsOut:
    base_where = [models.Response.restaurant_id == restaurant_id]
    window = _time_window_clause(from_, to_)
    if window is not None:
        base_where.append(window)

    # totales por action
    totals_stmt = (
        select(models.Response.action, func.count(models.Response.id))
        .where(*base_where)
        .group_by(models.Response.action)
    )
    totals = {action: count for action, count in db.execute(totals_stmt).all()}
    total_answered = totals.get("answered", 0)
    total_skipped = totals.get("skipped", 0)
    total_all = total_answered + total_skipped
    response_rate = (total_answered / total_all) if total_all else 0.0

    # avg rating y avg interaction_ms (sobre answered)
    aggs_stmt = select(
        func.avg(models.Response.rating),
        func.avg(models.Response.interaction_ms),
    ).where(*base_where, models.Response.action == "answered")
    avg_rating_raw, avg_interaction_raw = db.execute(aggs_stmt).one()
    avg_rating = float(avg_rating_raw) if avg_rating_raw is not None else 0.0
    avg_interaction_ms = (
        float(avg_interaction_raw) if avg_interaction_raw is not None else 0.0
    )

    # distribucion de ratings
    dist_stmt = (
        select(models.Response.rating, func.count(models.Response.id))
        .where(*base_where, models.Response.action == "answered")
        .group_by(models.Response.rating)
    )
    dist_rows = db.execute(dist_stmt).all()
    rating_distribution = {
        str(r): 0 for r in range(1, 6)
    }
    for rating, count in dist_rows:
        if rating is not None:
            rating_distribution[str(rating)] = count

    # by_category — join a questions
    cat_stmt = (
        select(
            models.Question.category,
            func.count(models.Response.id),
            func.avg(models.Response.rating),
        )
        .join(models.Question, models.Question.id == models.Response.question_id)
        .where(*base_where, models.Response.action == "answered")
        .group_by(models.Question.category)
    )
    by_category: dict[str, schemas.CategoryStats] = {}
    for category, count, avg in db.execute(cat_stmt).all():
        by_category[category] = schemas.CategoryStats(
            count=count,
            avg=float(avg) if avg is not None else 0.0,
        )

    # active alerts: no resueltas Y ultimas 24h
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    active_alerts_count = db.execute(
        select(func.count(models.Alert.id)).where(
            models.Alert.restaurant_id == restaurant_id,
            models.Alert.created_at >= since,
            models.Alert.resolved_at.is_(None),
        )
    ).scalar_one()

    return schemas.DashboardMetricsOut(
        total_responses=total_answered,
        total_skipped=total_skipped,
        response_rate=round(response_rate, 3),
        avg_rating=round(avg_rating, 2),
        avg_interaction_ms=round(avg_interaction_ms, 0),
        rating_distribution=rating_distribution,
        by_category=by_category,
        active_alerts=active_alerts_count,
    )


@router.get(
    "/responses/recent",
    response_model=list[schemas.RecentResponseOut],
)
def recent_responses(
    restaurant_id: uuid.UUID = Query(...),
    limit: int = Query(default=20, ge=1, le=200),
    db: Session = Depends(get_db),
) -> list[schemas.RecentResponseOut]:
    stmt = (
        select(
            models.Response.id,
            models.Response.rating,
            models.Response.action,
            models.Question.text,
            models.Question.category,
            models.Table.number,
            models.Waiter.name,
            models.Response.responded_at,
            models.Response.interaction_ms,
        )
        .join(
            models.Question,
            models.Question.id == models.Response.question_id,
            isouter=True,
        )
        .join(models.Table, models.Table.id == models.Response.table_id)
        .join(models.Waiter, models.Waiter.id == models.Response.waiter_id)
        .where(models.Response.restaurant_id == restaurant_id)
        .order_by(models.Response.created_at.desc())
        .limit(limit)
    )
    rows = db.execute(stmt).all()
    return [
        schemas.RecentResponseOut(
            id=r.id,
            rating=r.rating,
            action=r.action,
            question_text=r.text,
            category=r.category,
            table_number=r.number,
            waiter_name=r.name,
            responded_at=r.responded_at,
            interaction_ms=r.interaction_ms,
        )
        for r in rows
    ]


@router.get("/alerts", response_model=list[schemas.AlertOut])
def list_alerts(
    restaurant_id: uuid.UUID = Query(...),
    db: Session = Depends(get_db),
) -> list[schemas.AlertOut]:
    # Definicion de "alerta activa": no resuelta Y dentro de las ultimas 24h.
    since = datetime.now(timezone.utc) - timedelta(hours=24)
    stmt = (
        select(
            models.Alert.id,
            models.Alert.response_id,
            models.Alert.whatsapp_status,
            models.Alert.whatsapp_message_sid,
            models.Alert.sent_at,
            models.Alert.resolved_at,
            models.Alert.created_at,
            models.Response.rating,
            models.Table.number,
            models.Waiter.name,
            models.Question.text,
        )
        .join(models.Response, models.Response.id == models.Alert.response_id)
        .join(models.Table, models.Table.id == models.Response.table_id)
        .join(models.Waiter, models.Waiter.id == models.Response.waiter_id)
        .join(
            models.Question,
            models.Question.id == models.Response.question_id,
            isouter=True,
        )
        .where(
            models.Alert.restaurant_id == restaurant_id,
            models.Alert.created_at >= since,
            models.Alert.resolved_at.is_(None),
        )
        .order_by(models.Alert.created_at.desc())
    )
    return [
        schemas.AlertOut(
            id=r.id,
            response_id=r.response_id,
            whatsapp_status=r.whatsapp_status,
            whatsapp_message_sid=r.whatsapp_message_sid,
            sent_at=r.sent_at,
            resolved_at=r.resolved_at,
            created_at=r.created_at,
            rating=r.rating,
            table_number=r.number,
            waiter_name=r.name,
            question_text=r.text,
        )
        for r in db.execute(stmt).all()
    ]
