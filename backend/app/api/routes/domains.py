from fastapi import APIRouter

from app.services.demo_data import DOMAINS

router = APIRouter(tags=["domains"])


@router.get("/domains")
def get_domains():
    return {"domains": DOMAINS}