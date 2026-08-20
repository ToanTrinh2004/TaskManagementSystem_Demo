from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.db.session import get_db
from app.modules.workspaces.schemas import WorkSpaceCreate, WorkSpaceResponse
from app.modules.workspaces.service import WorkSpaceService
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user

bearer_scheme = HTTPBearer()
router = APIRouter(prefix="/workspaces", tags=["workspaces"])



@router.post("/", response_model=WorkSpaceResponse)
async def create_workspace(data: WorkSpaceCreate,db: AsyncSession = Depends(get_db),current_user=Depends(get_current_user)):
    service = WorkSpaceService(db)
    new_workspace = await service.create_workspace(data, current_user.id)
    return new_workspace