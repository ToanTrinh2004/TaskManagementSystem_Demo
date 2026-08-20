import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.modules.users.model import UserRole

class UserCreate(BaseModel):
    email : EmailStr
    full_name : str = Field( min_length=1, max_length=50)
    password : str = Field( min_length=8, max_length=100)

class UserResponse(BaseModel):
    id : uuid.UUID
    email : EmailStr
    full_name : str
    system_role: UserRole
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True

class LoginRequest(BaseModel):
    email : EmailStr
    password : str = Field( min_length=8, max_length=100)
class LoginResponse(BaseModel):
    access_token : str
    refresh_token : str
    token_type : str
class RefreshTokenResponse(BaseModel):
    access_token : str
    token_type : str

class RefreshRequest(BaseModel):
    refresh_token: str

