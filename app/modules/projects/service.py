import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ForbiddenError, NotFoundError
from app.modules.project_members.model import ProjectMember, ProjectRole
from app.modules.project_members.repository import ProjectMemberRepository
from app.modules.projects.model import Project
from app.modules.projects.repository import ProjectRepository
from app.modules.projects.schemas import ProjectCreate
from app.modules.workspace_members.model import WorkSpaceRole
from app.modules.workspace_members.repository import WorkSpaceMemberRepository
from app.modules.workspaces.repository import WorkSpaceRepository


class ProjectService:
    def __init__(self, db: AsyncSession):
        self.repo =ProjectRepository(db)
        self.project_member_repo = ProjectMemberRepository(db)
        self.workspace_repo = WorkSpaceRepository(db)
        self.workspace_member_repo = WorkSpaceMemberRepository(db)
        self.db = db 
    
    async def create_project(self, data: ProjectCreate, user_id: uuid.UUID):
        ## workspace must exist
        workspace = await self.workspace_repo.get_workspace_by_id(data.workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")
        ## user must be a member of the workspace
        member = await self.workspace_member_repo.get_member_by_id(user_id,data.workspace_id)
        print("member",member)
        print("user_id",user_id)
        print("workspace_id",data.workspace_id)
        if not member:
            raise ForbiddenError("User is not a member of the workspace")
        ## user must be a manager of the workspace or owner
        if member.role == WorkSpaceRole.MEMBER:
            raise ForbiddenError("You have no rights")
        project = Project(
            name=data.name,
            description=data.description,
            workspace_id=data.workspace_id,
            owner_id = user_id
        )
        result = await self.repo.create_project(project)

        leader = ProjectMember(
            project_id=result.id,
            user_id=user_id,
            role=ProjectRole.LEADER
        )

        await self.project_member_repo.create_member(leader)

        await self.db.commit()
        await self.db.refresh(result)
        return result
    
    async def get_project_by_id(self,project_id: uuid.UUID,  user_id:uuid.UUID):
        project =  await self.repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return project
        