from src.db.base_model import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON
from datetime import datetime, timezone
import enum
from typing import List


class CategoryEnum(str, enum.Enum):
    app = "app"
    patgpt_globalspace="patgpt_globalspace"
    data="data"
    billing_and_plans="billing_and_plans"

def utcnow():
    return datetime.now(timezone.utc)
class AboutPATGPT(Base):
    __tablename__ = "AboutPATGPT"

    id = Column(Integer, primary_key=True, autoincrement=True)
    category = Column(
        Enum(CategoryEnum, name="category_enum"),
        nullable=False,
        default=CategoryEnum.app,
    )
    data = Column(String(5000), nullable=False)
    keywords = Column(JSON, nullable=False, default=[])
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)
