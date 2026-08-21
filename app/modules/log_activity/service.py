import uuid
from app.modules.log_activity.model import ActivityAction, ActivityLog
from app.modules.log_activity.repository import ActivityLogRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ActivityLogService:

    def __init__(self, db: AsyncSession):
        self.repo = ActivityLogRepository(db)

    async def create_log(self, user_id: uuid.UUID, action: ActivityAction, project_id: uuid.UUID, target_id: uuid.UUID,
    ):
        log = ActivityLog(
            user_id=user_id,
            project_id=project_id,
            action=action,
            target_id=target_id,
        )

        return await self.repo.create(log)

    async def list_project_logs(self, project_id: uuid.UUID):
        return await self.repo.list_by_project(project_id)