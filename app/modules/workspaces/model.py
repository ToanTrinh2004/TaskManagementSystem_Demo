import uuid
from datetime import datetime
from sqlalchemy import ForeignKey, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class WorkSpace(Base):
    __tablename__ = "workspaces"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default= uuid.uuid4)
    name : Mapped[str] = mapped_column(String(50),nullable=False)
    description : Mapped[str] = mapped_column(String(200),nullable=False)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
   