import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import ForbiddenError, NotFoundError, UnauthorizedError, BadRequestError
from app.modules.workspace_members.repository import WorkSpaceMemberRepository
from app.modules.workspace_members.model import WorkSpaceMember, WorkSpaceRole
from app.modules.workspace_members.schemas import MemberInvite, MemberRoleUpdate
from app.modules.workspaces.repository import WorkSpaceRepository


class WorkSpaceMemberService:
    def __init__(self, db: AsyncSession):
        self.repo = WorkSpaceMemberRepository(db)
        self.workspace_repo = WorkSpaceRepository(db)
        self.db = db

    async def invite_member(self, workspace_id: uuid.UUID,data: MemberInvite, owner_id: uuid.UUID):
        workspace = await self.workspace_repo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")

        if workspace.owner_id != owner_id:
            raise ForbiddenError("You have no rights")

        check_member = await self.repo.get_member(workspace_id, data.user_id)
        if check_member:
            raise BadRequestError("User already a member of this workspace")

        member = WorkSpaceMember(
            workspace_id=workspace_id,
            user_id=data.user_id,
            role=WorkSpaceRole.MEMBER,
        )
        await self.repo.create_member(member)
        await self.db.commit()
        await self.db.refresh(member)
        return member
    

    async def list_members(self, workspace_id: uuid.UUID,page: int = 1,page_size: int = 20,):
        workspace = await self.workspace_repo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")
        return await self.repo.list_members(workspace_id,page,page_size)
    

    async def remove_member(self, workspace_id: uuid.UUID, user_id: uuid.UUID, owner_id: uuid.UUID):
        workspace = await self.workspace_repo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")

        if workspace.owner_id != owner_id:
            raise ForbiddenError("You have no rights")
        
        if workspace.owner_id == user_id:
            raise BadRequestError("Owner cannot be removed from workspace")

        member = await self.repo.get_member(workspace_id, user_id)
        if not member:
            raise NotFoundError("Member not found")

        await self.repo.delete_member(member)
        return {"message": "Deleted successfully"}

    async def update_member_role(self, workspace_id: uuid.UUID, user_id: uuid.UUID, data: MemberRoleUpdate, owner_id: uuid.UUID):

        workspace = await self.workspace_repo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")

        if workspace.owner_id != owner_id:
            raise ForbiddenError("You have no rights")
        print(user_id)

        member = await self.repo.get_member(workspace_id,user_id)
        print(member)
        if not member:
            raise NotFoundError("Member not found")
        member.role = WorkSpaceRole(data.role)
        result  = await self.repo.update_member(member)
        return result


