import asyncio
from pathlib import Path

import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from backend.database import Base, get_db
from backend.main import app
from backend.utils.config import BASE_DIR
from backend.services.challenge_service import seed_challenges

TEST_DB_URL = f"sqlite+aiosqlite:///{BASE_DIR}/test_aaj_kar_garne.db"

test_engine = create_async_engine(TEST_DB_URL, echo=False)
test_async_session = async_sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def override_get_db():
    async with test_async_session() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture(autouse=True)
async def setup_db():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with test_async_session() as db:
        await seed_challenges(db)
    yield
    await test_engine.dispose()
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    db_path = Path(str(BASE_DIR / "test_aaj_kar_garne.db"))
    if db_path.exists():
        try:
            db_path.unlink()
        except PermissionError:
            pass


@pytest_asyncio.fixture
async def client():
    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def token(client):
    resp = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "display_name": "Test User",
            "password": "test1234",
        },
    )
    data = resp.json()
    return data["access_token"]


@pytest_asyncio.fixture
async def auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


@pytest_asyncio.fixture
async def second_user_token(client):
    resp = await client.post(
        "/api/auth/register",
        json={
            "username": "frienduser",
            "display_name": "Friend User",
            "password": "test1234",
        },
    )
    return resp.json()["access_token"]
