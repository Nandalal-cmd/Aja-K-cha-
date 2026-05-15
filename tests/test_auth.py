import pytest


@pytest.mark.asyncio
async def test_register(client):
    resp = await client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "display_name": "New User",
            "password": "test1234",
        },
    )
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["user"]["username"] == "newuser"
    assert data["user"]["display_name"] == "New User"


@pytest.mark.asyncio
async def test_register_duplicate_username(client, token):
    resp = await client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "display_name": "Another",
            "password": "test1234",
        },
    )
    assert resp.status_code == 400
    assert "already taken" in resp.json()["detail"]


@pytest.mark.asyncio
async def test_login(client):
    await client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "display_name": "Login User",
            "password": "test1234",
        },
    )
    resp = await client.post(
        "/api/auth/login",
        json={"username": "loginuser", "password": "test1234"},
    )
    assert resp.status_code == 200
    assert "access_token" in resp.json()


@pytest.mark.asyncio
async def test_login_invalid(client):
    resp = await client.post(
        "/api/auth/login",
        json={"username": "nobody", "password": "wrong"},
    )
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_get_me(client, auth_headers):
    resp = await client.get("/api/auth/me", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["username"] == "testuser"
    assert data["display_name"] == "Test User"
    assert "streak" in data
    assert "friend_count" in data


@pytest.mark.asyncio
async def test_get_me_unauthorized(client):
    resp = await client.get("/api/auth/me")
    assert resp.status_code == 401


@pytest.mark.asyncio
async def test_update_profile(client, auth_headers):
    resp = await client.put(
        "/api/auth/me",
        json={"display_name": "Updated Name", "bio": "Hello world"},
        headers=auth_headers,
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["display_name"] == "Updated Name"
    assert data["bio"] == "Hello world"
