import os
import uuid

from fastapi import HTTPException, UploadFile, status

from app.core.config import get_settings


def validate_upload_file(file: UploadFile, file_size: int) -> None:
    settings = get_settings()
    allowed_extensions = {ext.strip() for ext in settings.allowed_file_extensions.split(",")}
    extension = os.path.splitext(file.filename or "")[1].lower()

    if extension not in allowed_extensions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported file type. Allowed: {', '.join(sorted(allowed_extensions))}",
        )

    max_size_bytes = settings.max_upload_size_mb * 1024 * 1024
    if file_size > max_size_bytes:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File too large. Max size is {settings.max_upload_size_mb} MB",
        )


def generate_stored_filename(original_name: str) -> str:
    extension = os.path.splitext(original_name)[1].lower()
    return f"{uuid.uuid4().hex}{extension}"
