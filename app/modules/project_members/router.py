from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.project_members.schemas import ProjectMemberInvite, ProjectMemberResponse
from app.modules.project_members.service import ProjectMemberService
from app.modules.projects import router


@router.post("/", response_model=ProjectMemberResponse)
async def invite_member(data: ProjectMemberInvite,db: AsyncSession = Depends(get_db),current_user=Depends(get_current_user)):
    service = ProjectMemberService(db)
    member = await service.invite_member(data,current_user.id,)
    return member