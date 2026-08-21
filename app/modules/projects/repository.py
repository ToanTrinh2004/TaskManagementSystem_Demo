import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.projects.model import Project


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_project(self, project):
        await self.db.add(project)
        await self.db.flush()
        return project
    
    async def get_project_by_id(self, project_id):
        query = select(Project).where(Project.id == project_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def update_project(self,project:Project):
        await self.db.add(project)
        await self.db.commit()
        await self.db.refresh(project)
        return project
    
    async def delete_project(self,project : Project):
        await self.db.delete(project)
        await self.db.commit()
        

    
    