import streamlit as st
import httpx
from typing import Optional

API_BASE = "http://localhost:8000/api"


def get_headers():
    token = st.session_state.get("token")
    if token:
        return {"Authorization": f"Bearer {token}"}
    return {}


def handle_response(response):
    if response.status_code == 401:
        st.session_state.token = None
        st.session_state.user = None
        st.rerun()
    return response


async def register(username, display_name, password):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{API_BASE}/auth/register",
            json={"username": username, "display_name": display_name, "password": password},
        )
        return handle_response(resp)


async def login(username, password):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{API_BASE}/auth/login",
            json={"username": username, "password": password},
        )
        return handle_response(resp)


async def get_me():
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{API_BASE}/auth/me", headers=get_headers())
        return handle_response(resp)


async def get_today_challenge():
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{API_BASE}/challenges/today", headers=get_headers())
        return handle_response(resp)


async def upload_post(challenge_id, caption, is_public, image_bytes, filename):
    async with httpx.AsyncClient(timeout=60) as client:
        files = {"image": (filename, image_bytes, "image/jpeg")}
        data = {"challenge_id": str(challenge_id), "caption": caption, "is_public": str(is_public)}
        resp = await client.post(
            f"{API_BASE}/posts/upload",
            headers={**get_headers(), "accept": "application/json"},
            data=data,
            files=files,
        )
        return handle_response(resp)


async def get_feed(skip=0, limit=20):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{API_BASE}/posts/feed",
            params={"skip": skip, "limit": limit},
            headers=get_headers(),
        )
        return handle_response(resp)


async def get_my_posts(skip=0, limit=20):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{API_BASE}/posts/my",
            params={"skip": skip, "limit": limit},
            headers=get_headers(),
        )
        return handle_response(resp)


async def delete_post(post_id):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.delete(
            f"{API_BASE}/posts/{post_id}",
            headers=get_headers(),
        )
        return handle_response(resp)


async def react_to_post(post_id, emoji):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{API_BASE}/posts/{post_id}/react",
            headers={**get_headers(), "accept": "application/json"},
            data={"emoji": emoji},
        )
        return handle_response(resp)


async def search_users(query, skip=0, limit=20):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{API_BASE}/friends/search",
            params={"q": query, "skip": skip, "limit": limit},
            headers=get_headers(),
        )
        return handle_response(resp)


async def send_friend_request(user_id):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{API_BASE}/friends/request/{user_id}",
            headers=get_headers(),
        )
        return handle_response(resp)


async def accept_friend_request(request_id):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{API_BASE}/friends/accept/{request_id}",
            headers=get_headers(),
        )
        return handle_response(resp)


async def reject_friend_request(request_id):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{API_BASE}/friends/reject/{request_id}",
            headers=get_headers(),
        )
        return handle_response(resp)


async def remove_friend(friend_id):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.delete(
            f"{API_BASE}/friends/{friend_id}",
            headers=get_headers(),
        )
        return handle_response(resp)


async def get_friends():
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{API_BASE}/friends/list", headers=get_headers())
        return handle_response(resp)


async def get_pending_requests():
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(f"{API_BASE}/friends/requests", headers=get_headers())
        return handle_response(resp)


async def upload_avatar(image_bytes, filename):
    async with httpx.AsyncClient(timeout=60) as client:
        files = {"image": (filename, image_bytes, "image/jpeg")}
        resp = await client.post(
            f"{API_BASE}/auth/avatar",
            headers={**get_headers(), "accept": "application/json"},
            files=files,
        )
        return handle_response(resp)


async def get_notifications(skip=0, limit=50):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{API_BASE}/notifications/",
            params={"skip": skip, "limit": limit},
            headers=get_headers(),
        )
        return handle_response(resp)


async def get_unread_count():
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            f"{API_BASE}/notifications/unread-count",
            headers=get_headers(),
        )
        return handle_response(resp)


async def mark_notification_read(notification_id):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{API_BASE}/notifications/{notification_id}/read",
            headers=get_headers(),
        )
        return handle_response(resp)


async def mark_all_notifications_read():
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            f"{API_BASE}/notifications/read-all",
            headers=get_headers(),
        )
        return handle_response(resp)


async def update_profile(data: dict):
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.put(
            f"{API_BASE}/auth/me",
            json=data,
            headers=get_headers(),
        )
        return handle_response(resp)
