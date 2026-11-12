from fastapi import APIRouter, Depends, HTTPException

from app.database import repository
from app.database.session import get_db_optional
from app.schemas.schemas import (
    InterviewSessionOut,
    SessionCreateRequest,
    SessionDetailOut,
)

router = APIRouter(tags=["sessions"])


@router.post("/sessions", response_model=InterviewSessionOut)
def create_session(payload: SessionCreateRequest, db=Depends(get_db_optional)):
    return repository.create_session(db, payload.domain, payload.level)


@router.get("/sessions", response_model=list[InterviewSessionOut])
def get_sessions(db=Depends(get_db_optional)):
    return repository.list_sessions(db)


@router.get("/sessions/{session_id}", response_model=SessionDetailOut)
def get_session(session_id: int, db=Depends(get_db_optional)):
    detail = repository.get_session_detail(db, session_id)
    if detail is None:
        raise HTTPException(status_code=404, detail="Session introuvable")
    return detail