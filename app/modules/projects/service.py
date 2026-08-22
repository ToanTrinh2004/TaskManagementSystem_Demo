import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.events import publish_event
from app.core.exceptions import ForbiddenError, NotFoundError
import redis.asyncio as redis
from app.modules.log_activity.model import ActivityAction
from app.modules.project_members.model import ProjectMember, ProjectRole
from app.modules.project_members.repository import ProjectMemberRepository
from app.modules.projects.model import Project
from app.modules.projects.repository import ProjectRepository
from app.modules.projects.schemas import ProjectCreate, ProjectUpdate
from app.modules.workspace_members.model import WorkSpaceRole
from app.modules.workspace_members.repository import WorkSpaceMemberRepository
from app.modules.workspaces.repository import WorkSpaceRepository



class ProjectService:
    def __init__(self, db: AsyncSession, redis_client: redis.Redis):
        self.repo =ProjectRepository(db)
        self.project_member_repo = ProjectMemberRepository(db)
        self.workspace_repo = WorkSpaceRepository(db)
        self.workspace_member_repo = WorkSpaceMemberRepository(db)
        self.db = db 
        self.redis = redis_client

    async def __check_exits_project(self,project_id:uuid.UUID):
        project =  await self.repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return project
    
    async def create_project(self, data: ProjectCreate, user_id: uuid.UUID):
        ## workspace must exist
        workspace = await self.workspace_repo.get_workspace_by_id(data.workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")
        ## user must be a member of the workspace
        member = await self.workspace_member_repo.get_member(data.workspace_id,user_id)
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
        project_id = result.id
        
        leader = ProjectMember(
            project_id=result.id,
            user_id=user_id,
            role=ProjectRole.LEADER
        )

        await self.project_member_repo.create_member(leader)

        await self.db.commit()
        await self.db.refresh(result)
        await publish_event(
            self.redis,
            event_name=ActivityAction.PROJECT_CREATED,
            payload={
                "user_id": str(user_id),
                "project_id": str(project_id),   
                "target_id": str(project_id),
    },
)
        return result
    
    async def get_project_by_id(self,project_id: uuid.UUID):
        project = await self.__check_exits_project(project_id)
        return project
    
    async def update_project(self,project_id,data:ProjectUpdate,user_id : uuid.UUID):
        project = await self.__check_exits_project(project_id)
        if project.owner_id != user_id:
            raise ForbiddenError("You have no rights")
        if data.name is not None:
            project.name = data.name
        if data.description is not None:
            project.description = data.description
        await self.repo.update_project(project)
        await publish_event(
            self.redis,
            event_name=ActivityAction.PROJECT_UPDATED,
            payload={
                "user_id": str(user_id),
                "project_id": str(project_id),   
                "target_id": str(project_id),})
        return  project
    
    async def delete_project(self,project_id: uuid.UUID, user_id: uuid.UUID):
        project =  await self.__check_exits_project(project_id)
        await self.repo.delete_project(project)
        await publish_event(
            self.redis,
            event_name=ActivityAction.PROJECT_DELETED,
            payload={
                "user_id": str(user_id),
                "project_id": str(project_id),   
                "target_id": str(project_id),})
        return{"message": "Deleted successfully"}
        
        