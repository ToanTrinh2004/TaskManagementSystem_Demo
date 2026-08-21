import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import DateTime, Enum, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class ProjectRole(str, PyEnum):
    LEADER = "leader"
    MEMBER = "member"


class ProjectMember(Base):
    __tablename__ = "project_members"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("projects.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"),nullable=False)
    role: Mapped[ProjectRole] = mapped_column(Enum(ProjectRole),nullable=False, default=ProjectRole.MEMBER)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())