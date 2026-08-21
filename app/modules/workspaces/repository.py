import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.projects.model import Project
from app.modules.workspaces.model import WorkSpace
class WorkSpaceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    async def create_workspace(self,workspace : WorkSpace):
        self.db.add(workspace)
        ## insert workspace into db not commit yet
        await self.db.flush()
        return workspace
    
    async def get_workspace_by_owner(self,user_id : uuid.UUID):
        query = select(WorkSpace).where(WorkSpace.owner_id == user_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_workspace_by_id(self, id:uuid.UUID):
        query = select(WorkSpace).where(WorkSpace.id == id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def list_projects_in_workspace(self,workspace_id: uuid.UUID,page: int = 1,page_size: int = 20,):
        query = select(Project).where(Project.workspace_id == workspace_id).offset((page - 1) * page_size).limit(page_size)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_workspace(self, workspace: WorkSpace):
        await self.db.add(workspace)
        await self.db.commit()
        await self.db.refresh(workspace)
        return workspace
    
    async def delete(self, workspace):
        await self.db.delete(workspace)
        await self.db.commit()