from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class CategoryEnum(str, Enum):
    food = "food"
    app = "app"
    electronics = "electronics"
    clothing = "clothing"
    books = "books"


class AboutPATGPTValidationSchema(BaseModel):
    category: CategoryEnum = Field(..., description="Category of the about patgpt")
    data: str = Field(..., min_length=1, max_length=5000, description="Data of the about patgpt")
    is_active: Optional[bool] = Field(True, description="Is active")


class AboutPATGPTUpdateSchema(BaseModel):
    category: Optional[CategoryEnum] = Field(None, description="Category of the about patgpt")
    data: Optional[str] = Field(None, min_length=1, max_length=5000, description="Data of the about patgpt")
    is_active: Optional[bool] = Field(None, description="Is active")


class AboutPATGPTResponseSchema(BaseModel):
    id: int
    category: CategoryEnum
    data: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


class PaginatedAboutPATGPTResponse(BaseModel):
    total: int
    page: int
    page_size: int
    results: list[AboutPATGPTResponseSchema]