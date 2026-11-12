from fastapi import APIRouter

from app.database.session import is_db_available

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {
        "status": "ok",
        "database": "postgresql" if is_db_available() else "demo-memory",
    }