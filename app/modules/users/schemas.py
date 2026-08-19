import uuid
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.modules.users.model import UserRole

class UserCreate(BaseModel):
    email : EmailStr
    full_name : str = Field( min_length=1, max_length=50)
    password : str = Field( min_length=8, max_length=50)

class UserResponse(BaseModel):
    id : uuid.UUID
    email : EmailStr
    full_name : str
    system_role: UserRole
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True