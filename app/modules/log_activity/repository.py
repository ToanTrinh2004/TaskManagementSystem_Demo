import uuid

from sqlalchemy import select
from app.modules.log_activity.model import ActivityLog
from app.modules.project_members.model import ProjectMember
from sqlalchemy.ext.asyncio import AsyncSession


class ActivityLogRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, log: ActivityLog):
        self.db.add(log)
        await self.db.flush()
        return log

    async def list_by_project(self, project_id: uuid.UUID):
        query = (select(ActivityLog).where(ActivityLog.project_id == project_id).order_by(ActivityLog.created_at.desc()))
        result = await self.db.execute(query)
        return result.scalars().all()