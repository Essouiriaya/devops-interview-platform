import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import answers, domains, health, questions, sessions
from app.core.config import settings
from app.database import session as db_session

logger = logging.getLogger("uvicorn")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # ÉTAPE 2.6 : tentative de connexion PostgreSQL au démarrage
    try:
        db_session.init_db()
        db_session.set_db_available(True)
        logger.info("PostgreSQL connecté, tables créées.")
    except Exception as e:
        db_session.set_db_available(False)
        logger.warning(f"PostgreSQL indisponible ({e}). Mode démo en mémoire activé.")
    yield


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, prefix=settings.API_PREFIX)
app.include_router(domains.router, prefix=settings.API_PREFIX)
app.include_router(questions.router, prefix=settings.API_PREFIX)
app.include_router(answers.router, prefix=settings.API_PREFIX)
app.include_router(sessions.router, prefix=settings.API_PREFIX)


@app.get("/health", tags=["health"])
def root_health():
    return {"status": "ok", "docs": "/docs"}