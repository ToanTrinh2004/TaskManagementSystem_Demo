import uuid
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictError
from app.modules.workspaces.repository import WorkSpaceRepository
from app.modules.workspaces.schemas import WorkSpaceCreate
from app.modules.workspaces.model import WorkSpace

class WorkSpaceService:
    def __init__(self, db: AsyncSession):
        self.repo =WorkSpaceRepository(db)
    
    async def create_workspace(self, data: WorkSpaceCreate, user_id: uuid.UUID):
        workspace = WorkSpace(
            owner_id=user_id,
            name=data.name,
            description=data.description,
        )
        return await self.repo.create(workspace)