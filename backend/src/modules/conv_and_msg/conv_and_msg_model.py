from src.db.base_model import Base

class Conversation(Base):
    __tablename__ = "conversation"

    conversation_id = Column(String, index=True)
    user_id = Column(String, index=True)
    started_on = Column(DateTime(timezone=True), default=utcnow, nullable=False)
    
class MessageTypeEnum(str, enum.Enum):
    user = "user"
    ai="ai"


class Message(Base):
    __tablename__ = "message"

    message_id = Column(String, index=True)
    conversation_id = Column(String, index=True)
    user_id = Column(String, index=True)
    message = Column(String, index=True)
    message_type=Column(Enum(MessageTypeEnum, name="message_type_enum"), nullable=False, default=MessageTypeEnum.user)
    created_on=Column(DateTime(timezone=True), default=utcnow, nullable=False)
    
    
    
    