import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class WorkSpaceRole(str, PyEnum):
    OWNER = "owner"
    MEMBER = "member"


class WorkSpaceMember(Base):
    __tablename__ = "workspace_members"

    id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    workspace_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("workspaces.id"),nullable=False)
    user_id : Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id"), nullable=False)
    role : Mapped[WorkSpaceRole] = mapped_column(Enum(WorkSpaceRole),nullable=False, default=WorkSpaceRole.MEMBER)
    created_at : Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())