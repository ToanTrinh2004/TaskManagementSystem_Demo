import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.modules.workspace_members.schemas import MemberInvite,MemberResponse
from app.modules.workspace_members.service import WorkSpaceMemberService

router = APIRouter(prefix="/workspaces", tags=["workspace_members"])


@router.post("/{workspace_id}/members", response_model=MemberResponse)
async def invite_member(workspace_id : uuid.UUID, data : MemberInvite, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    service = WorkSpaceMemberService(db)
    member = await service.invite_member(workspace_id, data, current_user.id)
    return member