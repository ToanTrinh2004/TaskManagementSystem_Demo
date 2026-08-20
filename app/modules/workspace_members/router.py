import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.modules.workspace_members.schemas import MemberInvite,MemberResponse
from app.modules.workspace_members.service import WorkSpaceMemberService

router = APIRouter(prefix="/workspaces", tags=["workspace_members"])


@router.post("/{workspace_id}/members", response_model=MemberResponse)
async def invite_member(workspace_id : uuid.UUID,data : MemberInvite,db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    service = WorkSpaceMemberService(db)
    member = await service.invite_member(workspace_id, data, current_user.id)
    return member


@router.get("/{workspace_id}/members", response_model=list[MemberResponse])
async def list_members(workspace_id: uuid.UUID,db: AsyncSession = Depends(get_db)):
    service = WorkSpaceMemberService(db)
    members = await service.list_members(workspace_id)
    return members


@router.delete("/{workspace_id}/members/{user_id}")
async def remove_member(workspace_id: uuid.UUID, user_id: uuid.UUID,db: AsyncSession = Depends(get_db),current_user=Depends(get_current_user)):
    service = WorkSpaceMemberService(db)
    result = await service.remove_member(workspace_id, user_id, current_user.id)
    return result