import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from backend.services.post_service import delete_expired_posts

logger = logging.getLogger(__name__)


async def cleanup_job(session_factory: async_sessionmaker):
    try:
        async with session_factory() as db:
            count = await delete_expired_posts(db)
            if count:
                logger.info(f"Cleaned up {count} expired post(s)")
    except Exception as e:
        logger.error(f"Cleanup error: {e}")


def start_cleanup_scheduler(session_factory: async_sessionmaker):
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        cleanup_job,
        "interval",
        minutes=60,
        args=[session_factory],
        id="post_cleanup",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Cleanup scheduler started (runs every 60 min)")
    return scheduler
