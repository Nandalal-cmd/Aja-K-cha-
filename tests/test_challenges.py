import pytest


@pytest.mark.asyncio
async def test_get_today_challenge(client, auth_headers):
    resp = await client.get("/api/challenges/today", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert "title_np" in data
    assert "title_en" in data
    assert "description_np" in data
    assert "description_en" in data
    assert data["points"] >= 10


@pytest.mark.asyncio
async def test_get_today_challenge_unauthorized(client):
    resp = await client.get("/api/challenges/today")
    assert resp.status_code == 401
