from src.db.base_model import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone

class AboutPATGPT(Base):
    __tablename__ = "AboutPATGPT"

    id = Column(Integer, primary_key=True)
    data = Column(String(500), nullable=False)
    category=Column(String(100))
    
    
    
    
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
