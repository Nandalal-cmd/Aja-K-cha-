# 🔥 Aaj K Garne? (आज के गर्ने?)

**Daily social challenge app for Nepali youth.** Get a new challenge each day, post photo/video proof, build streaks, and interact with friends through reactions.

## Tech Stack

- **Backend:** Python/FastAPI (async, SQLAlchemy async ORM, aiosqlite)
- **Frontend:** Python/Streamlit (multi-page)
- **Database:** SQLite
- **Auth:** JWT (python-jose) + bcrypt
- **Scheduler:** APScheduler for periodic cleanup of expired posts
- **Image processing:** Pillow

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run both backend and frontend
python run.py
```

- **Backend:** http://localhost:8000
- **Frontend:** http://localhost:8501
- **API docs:** http://localhost:8000/docs

## Running as an Application

### Double-click `run.py`
If `.py` files are associated with Python, just double-click `run.py`.

### Double-click `start_app.bat`
Double-click the batch file — it launches both servers and opens the frontend in your browser.

### Windows Shortcut (minimized console)
Create a shortcut with target:
```
C:\Windows\System32\cmd.exe /c "cd /d D:\Aja k Garne App && python run.py"
```
Set **Run → Minimized** in Properties to hide the console window.

### Standalone .exe (fully portable)
```bash
pip install pyinstaller
pyinstaller --onefile --name "AajKGarne" run.py
```
Run the generated `dist/AajKGarne.exe` anywhere — no Python required.

## Project Structure

```
├── run.py                     # Launches backend + frontend
├── run_backend.py             # Launches backend only
├── requirements.txt
├── backend/
│   ├── main.py                # FastAPI app entry point
│   ├── database.py            # SQLAlchemy async engine + session
│   ├── models.py              # 7 ORM models (User, Challenge, Post, Reaction, FriendRequest, Streak, Notification)
│   ├── schemas.py             # Pydantic request/response schemas
│   ├── routers/               # API route handlers
│   │   ├── auth.py            # Register, login, profile, avatar
│   │   ├── challenges.py      # Today's challenge
│   │   ├── posts.py           # Upload, feed, reactions
│   │   ├── friends.py         # Search, request, accept, reject
│   │   └── notifications.py   # List, read, unread count
│   ├── services/              # Business logic
│   └── utils/                 # Config, auth helpers, file uploads
├── frontend/
│   ├── app.py                 # Streamlit main app with sidebar nav
│   ├── components/            # Reusable UI components
│   │   ├── avatar.py          # Avatar (image or gradient initial)
│   │   ├── post_card.py       # Post card with reactions
│   │   ├── friend_item.py     # Friend list item
│   │   └── streak_badge.py    # Streak badge
│   ├── pages/                 # Streamlit pages
│   │   ├── login.py, register.py, home.py
│   │   ├── feed.py, friends.py, profile.py
│   │   └── notifications.py
│   └── utils/api_client.py    # HTTP client for backend APIs
├── uploads/                   # Uploaded images/videos
├── tests/                     # 20 pytest tests
└── aaj_kar_garne.db           # SQLite database (auto-created)
```

## API Endpoints

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/auth/register` | No | Register + return JWT |
| POST | `/api/auth/login` | No | Login + return JWT |
| GET | `/api/auth/me` | Yes | Current user profile |
| PUT | `/api/auth/me` | Yes | Update profile (name, bio, phone) |
| POST | `/api/auth/avatar` | Yes | Upload avatar image |
| GET | `/api/challenges/today` | Yes | Today's challenge |
| GET | `/api/challenges/{id}` | Yes | Challenge by ID |
| POST | `/api/posts/upload` | Yes | Upload photo/video for challenge |
| GET | `/api/posts/feed?skip=0&limit=20` | Yes | Paginated friends' feed |
| GET | `/api/posts/my?skip=0&limit=20` | Yes | Paginated user's posts |
| POST | `/api/posts/{id}/react` | Yes | React with emoji |
| GET | `/api/friends/search?q=&skip=0&limit=20` | Yes | Search users |
| POST | `/api/friends/request/{id}` | Yes | Send friend request |
| POST | `/api/friends/accept/{id}` | Yes | Accept request |
| POST | `/api/friends/reject/{id}` | Yes | Reject request |
| GET | `/api/friends/list` | Yes | List friends |
| GET | `/api/friends/requests` | Yes | Pending requests |
| GET | `/api/notifications/` | Yes | List notifications |
| GET | `/api/notifications/unread-count` | Yes | Unread count |
| POST | `/api/notifications/{id}/read` | Yes | Mark as read |
| POST | `/api/notifications/read-all` | Yes | Mark all read |
| GET | `/api/health` | No | Health check |

## Running Tests

```bash
python -m pytest tests/ -v
```

## Features

- 🇳🇵/🇬🇧 **Bilingual** — Toggle between Nepali and English
- 🎯 **Daily challenges** — Pre-seeded with 7+ bilingual challenges
- 📸 **Photo/video uploads** — Share proof of completed challenges
- 🔥 **Streak tracking** — Maintain daily streaks
- 👥 **Friend system** — Search, send requests, accept/reject
- 💜 **Reactions** — React to friends' posts with emojis
- 🔔 **Notifications** — Get notified on friend requests, accepts, and reactions
- 📱 **Paginated feed** — Load more posts as you scroll
- 👤 **Profile editing** — Update display name, bio, phone, avatar
- 🧹 **Auto-cleanup** — Expired posts (24h) are automatically removed
