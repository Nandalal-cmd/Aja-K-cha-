import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATABASE_URL = f"sqlite+aiosqlite:///{BASE_DIR}/aaj_kar_garne.db"

SECRET_KEY = "aaj-k-garne-super-secret-key-2024-nepal"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7

UPLOAD_DIR = BASE_DIR / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

POST_EXPIRY_HOURS = 24
CLEANUP_INTERVAL_MINUTES = 60
