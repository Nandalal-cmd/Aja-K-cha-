import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from backend.database import init_db, async_session
from backend.routers import auth, challenges, posts, friends, notifications
from backend.services.challenge_service import seed_challenges
from backend.services.cleanup_service import start_cleanup_scheduler
from backend.utils.config import UPLOAD_DIR

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    await init_db()
    async with async_session() as db:
        await seed_challenges(db)
    scheduler = start_cleanup_scheduler(async_session)
    yield
    scheduler.shutdown()
    logger.info("Shutting down...")


app = FastAPI(
    title="Aaj K Garne?",
    description="Daily challenge app for Nepali youth",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=str(UPLOAD_DIR)), name="uploads")

app.include_router(auth.router)
app.include_router(challenges.router)
app.include_router(posts.router)
app.include_router(friends.router)
app.include_router(notifications.router)


@app.get("/api/health")
async def health():
    return {"status": "ok", "app": "Aaj K Garne?"}
