import re
from pydantic import BaseModel, Field, EmailStr, field_validator

def _strong_password(v: str) -> str:
    if len(v) < 8:
        raise ValueError("Password must be at least 8 characters")
    if not re.search(r"[A-Z]", v):
        raise ValueError("Password must contain an uppercase letter")
    if not re.search(r"\d", v):
        raise ValueError("Password must contain a digit")
    return v

class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v): return _strong_password(v)

class UserUpdate(BaseModel):
    email: EmailStr | None = Field(default=None, max_length=120)
    password: str | None = Field(default=None, min_length=8)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v):
        return _strong_password(v) if v is not None else v

class AdminUserUpdate(BaseModel):
    role: str | None = None
    is_active: bool | None = None

class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8)

class RefreshRequest(BaseModel):
    refresh_token: str

class LogoutRequest(BaseModel):
    refresh_token: str