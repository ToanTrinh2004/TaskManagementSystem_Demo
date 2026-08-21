import uuid
from datetime import datetime
from enum import Enum as PyEnum
from sqlalchemy import DateTime, Enum, ForeignKey, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base



class ActivityLog(Base):
    __tablename__ = "activity_logs"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"),nullable=False)
    project_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True),ForeignKey("projects.id"),nullable=True)
    action: Mapped[str] = mapped_column(String(50),nullable=False)
    target_id: Mapped[uuid.UUID | None] = mapped_column(UUID(as_uuid=True),nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(),)

class ActivityAction(str, PyEnum):
    TASK_CREATED = "task_created"
    TASK_UPDATED = "task_updated"
    TASK_DELETED = "task_deleted"
    TASK_STATUS_CHANGED = "task_status_changed"

    PROJECT_CREATED = "project_created"
    PROJECT_UPDATED = "project_updated"
    PROJECT_DELETED = "project_deleted"

    MEMBER_INVITED = "member_invited"
    MEMBER_REMOVED = "member_removed"