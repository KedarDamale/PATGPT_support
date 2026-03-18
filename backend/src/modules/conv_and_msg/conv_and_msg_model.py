from src.db.base_model import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, timezone


def utcnow():
    return datetime.now(timezone.utc)


class Conversation(Base):
    __tablename__ = "Conversations"

    id = Column(String(36), primary_key=True)   
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String(200), nullable=True)   
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    updated_at = Column(DateTime(timezone=True), default=utcnow, onupdate=utcnow, nullable=False)

    messages = relationship("Message", back_populates="conversation",
                            order_by="Message.created_at", cascade="all, delete-orphan")


class MessageTypeEnum(str, enum.Enum):
    user = "user"
    ai="ai"

class Message(Base):
    __tablename__ = "Messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String(36), ForeignKey("Conversations.id", ondelete="CASCADE"),
                             nullable=False)
    role = Column(ENUM(MessageTypeEnumy, name="message_type_enum"), nullable=False)   
    content = Column(String(20000), nullable=False)
    created_at = Column(DateTime(timezone=True), default=utcnow, nullable=False)

    conversation = relationship("Conversation", back_populates="messages")