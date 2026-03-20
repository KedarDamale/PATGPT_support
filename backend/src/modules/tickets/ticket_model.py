from src.db.base_model import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum, JSON
from datetime import datetime, timezone
import enum
from typing import List

class TicketStatus(str, enum.Enum):
    open = "open"
    viewed="viewed"
    pending="pending"
    closed="closed"

def utcnow():
    return datetime.now(timezone.utc)

class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(5000), nullable=False)
    status = Column(Enum(TicketStatus), default=TicketStatus.open, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)