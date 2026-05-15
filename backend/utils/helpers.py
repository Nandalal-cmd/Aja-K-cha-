import datetime
import uuid
from pathlib import Path
from fastapi import UploadFile
from PIL import Image
import io

from backend.utils.config import UPLOAD_DIR


IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
VIDEO_EXTENSIONS = {"mp4", "mov", "avi", "mkv", "webm"}


async def save_upload(file: UploadFile) -> str:
    ext = (file.filename.split(".")[-1] if "." in file.filename else "jpg").lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    file_path = UPLOAD_DIR / filename

    contents = await file.read()

    if ext in IMAGE_EXTENSIONS:
        img = Image.open(io.BytesIO(contents))
        img.thumbnail((1080, 1080), Image.Resampling.LANCZOS)
        img.save(file_path, optimize=True, quality=85)
    elif ext in VIDEO_EXTENSIONS:
        with open(file_path, "wb") as f:
            f.write(contents)
    else:
        with open(file_path, "wb") as f:
            f.write(contents)

    return str(file_path)


async def save_avatar(file: UploadFile) -> str:
    ext = file.filename.split(".")[-1] if "." in file.filename else "jpg"
    filename = f"avatar_{uuid.uuid4().hex}.{ext}"
    file_path = UPLOAD_DIR / filename

    contents = await file.read()
    img = Image.open(io.BytesIO(contents))
    img.thumbnail((400, 400), Image.Resampling.LANCZOS)
    img.save(file_path, optimize=True, quality=90)

    return str(file_path)


def delete_file(file_path: str):
    path = Path(file_path)
    if path.exists():
        path.unlink()


def get_expiry_time(hours: int = 24) -> datetime.datetime:
    return datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
