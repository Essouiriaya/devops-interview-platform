from fastapi import Depends, APIRouter

from app.database import repository
from app.database.session import get_db_optional
from app.schemas.schemas import AnswerEvaluateRequest, EvaluationOut
from app.services import ai_service

router = APIRouter(tags=["answers"])


@router.post("/answers/evaluate", response_model=EvaluationOut)
def evaluate(payload: AnswerEvaluateRequest, db=Depends(get_db_optional)):
    result = ai_service.evaluate_answer(payload.question, payload.answer, payload.domain, payload.level)
    if payload.session_id is not None:
        repository.add_answer(
            db, payload.session_id, payload.question_id,
            payload.question, payload.answer, result,
        )
    return result