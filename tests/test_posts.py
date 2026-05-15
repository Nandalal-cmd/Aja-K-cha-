import io
import pytest
from PIL import Image


def _make_test_image():
    buf = io.BytesIO()
    img = Image.new("RGB", (100, 100), color="red")
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf


@pytest.mark.asyncio
async def test_upload_post(client, auth_headers):
    resp = await client.get("/api/challenges/today", headers=auth_headers)
    challenge_id = resp.json()["id"]

    img = _make_test_image()
    resp = await client.post(
        "/api/posts/upload",
        headers=auth_headers,
        data={"challenge_id": str(challenge_id), "caption": "Test post", "is_public": "True"},
        files={"image": ("test.jpg", img, "image/jpeg")},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["caption"] == "Test post"
    assert data["challenge_id"] == challenge_id


@pytest.mark.asyncio
async def test_get_my_posts(client, auth_headers):
    resp = await client.get("/api/challenges/today", headers=auth_headers)
    challenge_id = resp.json()["id"]

    img = _make_test_image()
    await client.post(
        "/api/posts/upload",
        headers=auth_headers,
        data={"challenge_id": str(challenge_id), "caption": "My post", "is_public": "True"},
        files={"image": ("test.jpg", img, "image/jpeg")},
    )

    resp = await client.get("/api/posts/my", headers=auth_headers)
    assert resp.status_code == 200
    posts = resp.json()
    assert len(posts) >= 1


@pytest.mark.asyncio
async def test_feed_empty(client, auth_headers, second_user_token):
    friend_headers = {"Authorization": f"Bearer {second_user_token}"}

    resp = await client.get("/api/posts/feed", headers=friend_headers)
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.asyncio
async def test_react_to_post(client, auth_headers):
    resp = await client.get("/api/challenges/today", headers=auth_headers)
    challenge_id = resp.json()["id"]

    img = _make_test_image()
    resp = await client.post(
        "/api/posts/upload",
        headers=auth_headers,
        data={"challenge_id": str(challenge_id), "caption": "Reactable", "is_public": "True"},
        files={"image": ("test.jpg", img, "image/jpeg")},
    )
    post_id = resp.json()["id"]

    resp = await client.post(
        f"/api/posts/{post_id}/react",
        headers=auth_headers,
        data={"emoji": "🔥"},
    )
    assert resp.status_code == 200
    assert resp.json()["emoji"] == "🔥"


@pytest.mark.asyncio
async def test_react_twice(client, auth_headers):
    resp = await client.get("/api/challenges/today", headers=auth_headers)
    challenge_id = resp.json()["id"]

    img = _make_test_image()
    resp = await client.post(
        "/api/posts/upload",
        headers=auth_headers,
        data={"challenge_id": str(challenge_id), "caption": "Double react", "is_public": "True"},
        files={"image": ("test.jpg", img, "image/jpeg")},
    )
    post_id = resp.json()["id"]

    await client.post(
        f"/api/posts/{post_id}/react",
        headers=auth_headers,
        data={"emoji": "🔥"},
    )
    resp = await client.post(
        f"/api/posts/{post_id}/react",
        headers=auth_headers,
        data={"emoji": "🔥"},
    )
    assert resp.status_code == 400
