from fastapi import APIRouter, Depends

from app.database import repository
from app.database.session import get_db_optional
from app.schemas.schemas import (
    QuestionGenerateRequest,
    QuestionOut,
)
from app.services import ai_service, demo_data

router = APIRouter(tags=["questions"])


@router.get("/questions")
def get_questions(domain: str, level: str = "intermédiaire"):
    """Questions de démo statiques (avant génération IA)."""
    return {"questions": demo_data.generate_demo_questions(domain, level, 5)}


@router.post("/questions/generate", response_model=list[QuestionOut])
def generate_questions(payload: QuestionGenerateRequest, db=Depends(get_db_optional)):
    questions = ai_service.generate_questions(payload.domain, payload.level, payload.count)
    if payload.session_id is not None:
        return repository.add_questions(db, payload.session_id, questions)
    return questions