import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.exceptions import NotFoundError, UnauthorizedError, BadRequestError
from app.modules.workspace_members.repository import WorkSpaceMemberRepository
from app.modules.workspace_members.model import WorkSpaceMember, WorkSpaceRole
from app.modules.workspace_members.schemas import MemberInvite
from app.modules.workspaces.repository import WorkSpaceRepository


class WorkSpaceMemberService:
    def __init__(self, db: AsyncSession):
        self.repo = WorkSpaceMemberRepository(db)
        self.workspace_repo = WorkSpaceRepository(db)

    async def invite_member(self, workspace_id: uuid.UUID, data: MemberInvite, requester_id: uuid.UUID):
        workspace = await self.workspace_repo.get_workspace_by_id(workspace_id)
        if not workspace:
            raise NotFoundError("Workspace not found")

        if workspace.owner_id != requester_id:
            raise UnauthorizedError("You have no rights")

        check_member = await self.repo.get_member(workspace_id, data.user_id)
        if check_member:
            raise BadRequestError("User already a member of this workspace")

        member = WorkSpaceMember(
            workspace_id=workspace_id,
            user_id=data.user_id,
            role=data.role,
        )
        return await self.repo.create_member(member)