import uuid
from app.core.exceptions import BadRequestError, ForbiddenError, NotFoundError
from app.modules.project_members.model import ProjectMember, ProjectRole
from app.modules.project_members.repository import ProjectMemberRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.project_members.schemas import ProjectMemberInvite
from app.modules.projects.repository import ProjectRepository
from app.modules.workspace_members.model import WorkSpaceRole
from app.modules.workspace_members.repository import WorkSpaceMemberRepository

class ProjectMemberService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = ProjectMemberRepository(db)
        self.project_repo = ProjectRepository(db)
        self.workspace_member_repo = WorkSpaceMemberRepository(db)

    async def __check_exits_project(self,project_id:uuid.UUID):
        project =  await self.project_repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return project

    async def invite_member(self,project_id:uuid.UUID,data: ProjectMemberInvite,owner_id : uuid.UUID):
        ## check is project exits 
        project = await self.__check_exits_project(project_id)
        ## check role
        if project.owner_id !=  owner_id:
            raise ForbiddenError("You have no rights")
        ## check member is in a same workspace with project
        member =  await self.workspace_member_repo.get_member(project.workspace_id,data.member_id)
        if not member :
            raise ForbiddenError("User is not workspace member")
        ## check is member in project already
        exits_member =  await self.repo.get_project_member_by_id(data.member_id,project_id)
        if exits_member is not None:
            raise BadRequestError("User already in project")
        
        new_member = ProjectMember(
            project_id = project_id,
            user_id = data.member_id,
            role = ProjectRole.MEMBER
        )
        await self.repo.create_member(new_member)
        await self.db.commit()
        await self.db.refresh(new_member)
        return new_member
        

    async def list_member(self,project_id : uuid.UUID):
        await self.__check_exits_project(project_id)
        return await self.repo.list_member(project_id)
    
    async def remove_member(self,project_id:uuid.UUID,member_id:uuid.UUID,owner_id:uuid.UUID):
        project = await self.__check_exits_project(project_id)
        if project.owner_id != owner_id :
            raise ForbiddenError("You have no rights")
        member =  await self.repo.get_project_member_by_id(member_id,project_id)
        if member is None:
            raise BadRequestError("User not in project")
        await self.repo.delete_member(member)
        return {"message": "Deleted successfully"}
        




        

