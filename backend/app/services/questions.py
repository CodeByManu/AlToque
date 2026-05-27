"""
Seleccion de la pregunta que se muestra al cerrar una mesa.

SPEC §6 dice:
  "Selección de pregunta: al llamar /sessions/start, el backend elige UNA
   pregunta del pool activo del restaurante con probabilidad uniforme.
   Si una pregunta tuvo <X respuestas recientes y otras >Y, preferir la
   menos respondida (round-robin ponderado). Para MVP: random uniforme
   está OK."

Esta funcion vive aislada del router a proposito: cuando quieras pasar de
random uniforme a round-robin ponderado, tocas un solo archivo.
"""
import logging
import random
import uuid

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app import models

logger = logging.getLogger(__name__)


def pick_question(db: Session, restaurant_id: uuid.UUID) -> models.Question | None:
    """
    Round-robin ponderado: elige la pregunta activa con menos respuestas
    historicas. Entre empatadas, desempata aleatoriamente.
    """
    stmt = (
        select(models.Question, func.count(models.Response.id).label("n"))
        .join(
            models.Response,
            models.Response.question_id == models.Question.id,
            isouter=True,
        )
        .where(models.Question.restaurant_id == restaurant_id)
        .where(models.Question.active.is_(True))
        .group_by(models.Question.id)
        .order_by(func.count(models.Response.id).asc())
    )
    rows = db.execute(stmt).all()
    if not rows:
        return None

    min_count = rows[0][1]
    candidates = [q for q, n in rows if n == min_count]
    chosen = random.choice(candidates)
    logger.info(
        "pick_question: elegida %s (n=%d, %d empatadas)",
        chosen.id,
        min_count,
        len(candidates),
    )
    return chosen
