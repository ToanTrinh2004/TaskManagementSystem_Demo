import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError
from app.modules.projects.model import Project
from app.modules.projects.repository import ProjectRepository
from app.modules.projects.schemas import ProjectCreate


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo =ProjectRepository(db)
    
    async def create_project(self, data: ProjectCreate, user_id: uuid.UUID):
        workspace = await self.repo.get_workspace_by_id(data.workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")
        project = Project(
            name=data.name,
            description=data.description,
            workspace_id=data.workspace_id,
        )
        result = await self.repo.create_project(project)
        return result