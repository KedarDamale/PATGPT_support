from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class UserMemoryResponseSchema(BaseModel):
    id: int
    user_id: int
    key: str
    value: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserMemoryUpdateSchema(BaseModel):
    value: str = Field(..., min_length=1, max_length=2000)


class PaginatedMemoryResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[UserMemoryResponseSchema]