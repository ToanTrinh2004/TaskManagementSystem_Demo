import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError
from app.modules.project_members.model import ProjectMember, ProjectRole
from app.modules.project_members.repository import ProjectMemberRepository
from app.modules.projects.model import Project
from app.modules.projects.repository import ProjectRepository
from app.modules.projects.schemas import ProjectCreate


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo =ProjectRepository(db)
        self.project_member_repo = ProjectMemberRepository(db)
    
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

        leader = ProjectMember(
            project_id=result.id,
            user_id=user_id,
            role=ProjectRole.LEADER
        )

        await self.project_member_repo.create_member(leader)

        await self.repo.commit()


        return result