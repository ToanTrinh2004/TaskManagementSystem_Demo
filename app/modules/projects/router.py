from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.projects.schemas import ProjectCreate, ProjectResponse
from app.modules.projects.service import ProjectService


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
async def create_project(data: ProjectCreate,db: AsyncSession = Depends(get_db),current_user=Depends(get_current_user)):
    service = ProjectService(db)
    new_workspace = await service.create_project(data, current_user.id)
    return new_workspace

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = ProjectService(db)
    project = await service.get_project_by_id(project_id,current_user.id)
    return project