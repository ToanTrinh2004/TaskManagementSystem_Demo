import uuid
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ConflictError, NotFoundError, UnauthorizedError
from app.modules.workspaces.repository import WorkSpaceRepository
from app.modules.workspaces.schemas import WorkSpaceCreate, WorkSpaceUpdate
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
        result = await self.repo.create_workspace(workspace)
        return result
    
    async def get_workspace_by_owner(self, user_id: uuid.UUID):
        workspace = await self.repo.get_workspace_by_owner(user_id)
        return workspace
    
    async def get_workspace(self, id: uuid.UUID):
        workspace = await self.repo.get_workspace_by_id(id)
        if not workspace:
            raise NotFoundError("Workspace not found")
        return workspace
    
    async def update_workspace(self, id: uuid.UUID, data : WorkSpaceUpdate , user_id: uuid.UUID):
        workspace = await self.repo.get_workspace_by_id(id)
        if not workspace:
            raise NotFoundError("Workspace not found")

        if workspace.owner_id != user_id:
            raise UnauthorizedError("You have no rights")

        if data.name is not None:
            workspace.name = data.name
        if data.description is not None:
            workspace.description = data.description

        new_workspace = await self.repo.update_workspace(workspace)

        return new_workspace
    
    async def delete_workspace(self, id: uuid.UUID, user_id: uuid.UUID):
        workspace = await self.repo.get_workspace_by_id(id)
        if not workspace:
            raise NotFoundError("Workspace not found")

        if workspace.owner_id != user_id:
            raise UnauthorizedError("You have no rights")

        await self.repo.delete(workspace)
        return {"message": "Deleted successfully"}