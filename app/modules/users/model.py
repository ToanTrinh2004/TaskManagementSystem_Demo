import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import String, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class UserRole(str,PyEnum):
    ADMIN = "admin"
    USER = "user"



class User(Base):
    __tablename__ = "users"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default= uuid.uuid4)
    email : Mapped[str] = mapped_column(String(50),unique=True,nullable=False)
    full_name : Mapped[str] = mapped_column(String(50),nullable=False)
    password : Mapped[str] = mapped_column(String(100),nullable=False)
    system_role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.USER)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now())

