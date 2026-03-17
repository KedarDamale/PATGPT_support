from pydantic import BaseModel, Field, EmailStr

#schema validation for creating user
class UserCreate(BaseModel):
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8)

# #schema validation for updating user
# class UserUpdate(BaseModel):
#     email: EmailStr | None = Field(default=None, max_length=120)

#schema validation for user output
class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

#schema validation before sending token
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

#schema validation for login request
class LoginRequest(BaseModel):
    email: EmailStr = Field(max_length=120)
    password: str = Field(min_length=8)

#schema validation for refresh request
class RefreshRequest(BaseModel):
    refresh_token: str
