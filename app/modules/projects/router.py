from typing import List
import uuid
from fastapi import APIRouter, Depends
import redis
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.dependencies import get_current_user
from app.db.redis_client import get_redis
from app.db.session import get_db
from app.modules.project_members.schemas import ProjectMemberInvite, ProjectMemberResponse
from app.modules.project_members.service import ProjectMemberService
from app.modules.projects.schemas import ProjectCreate, ProjectResponse, ProjectUpdate
from app.modules.projects.service import ProjectService


router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse)
async def create_project(data: ProjectCreate,db: AsyncSession = Depends(get_db),current_user=Depends(get_current_user),redis_client: redis.Redis = Depends(get_redis)):
    service = ProjectService(db, redis_client)
    new_workspace = await service.create_project(data, current_user.id)
    return new_workspace

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: uuid.UUID, db: AsyncSession = Depends(get_db),redis_client: redis.Redis = Depends(get_redis)):
    service = ProjectService(db, redis_client)
    project = await service.get_project_by_id(project_id)
    return project

@router.patch("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: uuid.UUID,data: ProjectUpdate, db: AsyncSession = Depends(get_db),current_user=Depends(get_current_user),redis_client: redis.Redis = Depends(get_redis)):
    service = ProjectService(db, redis_client)
    project = await service.update_project(project_id,data,current_user.id,)
    return project

@router.delete("/{project_id}")
async def delete_project(project_id: uuid.UUID,db: AsyncSession = Depends(get_db),current_user=Depends(get_current_user),redis_client: redis.Redis = Depends(get_redis)):
    service = ProjectService(db, redis_client)
    result = await service.delete_project(project_id,current_user.id,)
    return result


## workspace_member route

@router.post("/{project_id}/members", response_model=ProjectMemberResponse)
async def invite_member(data: ProjectMemberInvite,project_id: uuid.UUID,db: AsyncSession = Depends(get_db),current_user=Depends(get_current_user)):
    service = ProjectMemberService(db)
    member = await service.invite_member(project_id,data,current_user.id,)
    return member

@router.get("/{project_id}/members", response_model=List[ProjectMemberResponse])
async def list_member(project_id: uuid.UUID, page: int = 1, page_size: int = 20, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    service = ProjectMemberService(db)
    members = await service.list_member(project_id,page,page_size)
    return members

@router.delete("/{project_id}/members/{user_id}")
async def remove_member(project_id: uuid.UUID , user_id: uuid.UUID , db: AsyncSession = Depends(get_db) , current_user= Depends(get_current_user)):
    service = ProjectMemberService(db)
    result = await service.remove_member(project_id, user_id, current_user.id)
    return result