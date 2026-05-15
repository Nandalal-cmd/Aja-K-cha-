import pytest


@pytest.mark.asyncio
async def test_search_users(client, auth_headers, second_user_token):
    resp = await client.get("/api/friends/search?q=friend", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["users"]) >= 1
    assert any(u["username"] == "frienduser" for u in data["users"])


@pytest.mark.asyncio
async def test_send_friend_request(client, auth_headers, second_user_token):
    resp = await client.get("/api/friends/search?q=friend", headers=auth_headers)
    friend_id = resp.json()["users"][0]["id"]

    resp = await client.post(
        f"/api/friends/request/{friend_id}",
        headers=auth_headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "pending"


@pytest.mark.asyncio
async def test_accept_friend_request(client, auth_headers, second_user_token):
    resp = await client.get("/api/friends/search?q=friend", headers=auth_headers)
    friend_id = resp.json()["users"][0]["id"]

    await client.post(f"/api/friends/request/{friend_id}", headers=auth_headers)

    friend_headers = {"Authorization": f"Bearer {second_user_token}"}
    resp = await client.get("/api/friends/requests", headers=friend_headers)
    requests = resp.json()
    assert len(requests) >= 1
    req_id = requests[0]["id"]

    resp = await client.post(f"/api/friends/accept/{req_id}", headers=friend_headers)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Friend request accepted"


@pytest.mark.asyncio
async def test_reject_friend_request(client, auth_headers, second_user_token):
    resp = await client.get("/api/friends/search?q=friend", headers=auth_headers)
    friend_id = resp.json()["users"][0]["id"]

    await client.post(f"/api/friends/request/{friend_id}", headers=auth_headers)

    friend_headers = {"Authorization": f"Bearer {second_user_token}"}
    resp = await client.get("/api/friends/requests", headers=friend_headers)
    req_id = resp.json()[0]["id"]

    resp = await client.post(f"/api/friends/reject/{req_id}", headers=friend_headers)
    assert resp.status_code == 200


@pytest.mark.asyncio
async def test_friends_list(client, auth_headers, second_user_token):
    resp = await client.get("/api/friends/search?q=friend", headers=auth_headers)
    friend_id = resp.json()["users"][0]["id"]

    await client.post(f"/api/friends/request/{friend_id}", headers=auth_headers)

    friend_headers = {"Authorization": f"Bearer {second_user_token}"}
    resp = await client.get("/api/friends/requests", headers=friend_headers)
    req_id = resp.json()[0]["id"]
    await client.post(f"/api/friends/accept/{req_id}", headers=friend_headers)

    resp = await client.get("/api/friends/list", headers=auth_headers)
    assert resp.status_code == 200
    friends = resp.json()
    assert any(f["username"] == "frienduser" for f in friends)


@pytest.mark.asyncio
async def test_health(client):
    resp = await client.get("/api/health")
    assert resp.status_code == 200
    assert resp.json()["status"] == "ok"
