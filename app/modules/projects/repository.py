from sqlalchemy.ext.asyncio import AsyncSession


class ProjectRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create_project(self, project):
        self.db.add(project)
        await self.db.flush()
        return project