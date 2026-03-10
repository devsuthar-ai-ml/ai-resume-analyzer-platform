from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResumeUploadResponse(BaseModel):
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    created_at: datetime


class ResumeHistoryItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    original_filename: str
    file_type: str
    file_size: int
    created_at: datetime


class ResumeHistoryResponse(BaseModel):
    items: list[ResumeHistoryItem]
