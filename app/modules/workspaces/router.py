import uuid
from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer
from app.db.session import get_db
from app.modules.projects.schemas import ProjectResponse
from app.modules.workspaces.schemas import WorkSpaceCreate, WorkSpaceResponse, WorkSpaceUpdate
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

@router.get("/{id}", response_model=WorkSpaceResponse)
async def get_workspace(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    service = WorkSpaceService(db)
    workspace = await service.get_workspace(id)
    return workspace

@router.patch("/{id}", response_model=WorkSpaceResponse)
async def update_workspace(id: uuid.UUID, data: WorkSpaceUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = WorkSpaceService(db)
    workspace = await service.update_workspace(id, data, current_user.id)
    return workspace


@router.delete("/{id}")
async def delete_workspace(id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = WorkSpaceService(db)
    result = await service.delete_workspace(id, current_user.id)
    return result

@router.get("/{workspace_id}/projects",response_model=list[ProjectResponse])
async def list_projects(workspace_id: uuid.UUID, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = WorkSpaceService(db)
    projects = await service.list_projects_in_workspace(workspace_id, current_user.id)
    return projects