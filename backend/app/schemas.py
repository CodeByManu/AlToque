from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


# --- Sessions ---

class QuestionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    text: str
    category: str


class SessionStartOut(BaseModel):
    session_id: UUID
    question: QuestionOut
    shown_at: datetime


# --- Responses ---

class ResponseCreate(BaseModel):
    session_id: UUID
    question_id: UUID | None = None  # NULL si action="skipped"
    rating: int | None = Field(default=None, ge=1, le=5)
    action: Literal["answered", "skipped"]
    shown_at: datetime
    responded_at: datetime


class ResponseOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    restaurant_id: UUID
    table_id: UUID
    waiter_id: UUID
    question_id: UUID | None
    rating: int | None
    action: str
    shown_at: datetime
    responded_at: datetime
    interaction_ms: int
    created_at: datetime


# --- Dashboard ---

class CategoryStats(BaseModel):
    count: int
    avg: float


class DashboardMetricsOut(BaseModel):
    total_responses: int
    total_skipped: int
    response_rate: float
    avg_rating: float
    avg_interaction_ms: float
    rating_distribution: dict[str, int]
    by_category: dict[str, CategoryStats]
    active_alerts: int


class RecentResponseOut(BaseModel):
    id: UUID
    rating: int | None
    action: str
    question_text: str | None
    category: str | None
    table_number: int
    waiter_name: str
    responded_at: datetime
    interaction_ms: int


class AlertOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    response_id: UUID
    whatsapp_status: str
    whatsapp_message_sid: str | None
    sent_at: datetime | None
    resolved_at: datetime | None
    created_at: datetime
    # Contexto util para el dashboard
    rating: int | None = None
    table_number: int | None = None
    waiter_name: str | None = None
    question_text: str | None = None


class RestaurantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


# --- Admin ---

class SeedOut(BaseModel):
    restaurant_id: UUID
    waiters: int
    tables: int
    questions: int
