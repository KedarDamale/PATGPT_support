from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class MessageSchema(BaseModel):
    id: int
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class ConversationSummarySchema(BaseModel):
    """Used in list view — no messages loaded."""
    id: str
    title: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationDetailSchema(ConversationSummarySchema):
    """Used in detail view — full message thread."""
    messages: list[MessageSchema] = []


class ChatRequestSchema(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[str] = Field(
        None,
        description="Omit to start a new conversation. Send existing ID to continue one."
    )


class ChatResponseSchema(BaseModel):
    conversation_id: str
    title: Optional[str]
    reply: str