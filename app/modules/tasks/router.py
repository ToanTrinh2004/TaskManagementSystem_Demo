from typing import Optional
import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user, get_redis
from app.db.session import get_db
from app.modules.tasks.schemas import TaskCreate, TaskResponse, TaskStatusUpdate, TaskUpdate
from app.modules.tasks.service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/{project_id}/tasks", response_model=TaskResponse)
async def create_task(data: TaskCreate, project_id: uuid.UUID, db: AsyncSession = Depends(get_db), redis=Depends(get_redis), current_user=Depends(get_current_user)):
    service = TaskService(db, redis)
    task = await service.create_task(project_id, data, current_user.id)
    return task


@router.get("/{project_id}/tasks")
async def list_tasks(project_id: uuid.UUID, page: int = 1, page_size: int = 20, status: Optional[str] = None, priority: Optional[str] = None, assignee_id: Optional[uuid.UUID] = None, sort_by: str = "created_at", order: str = "desc", db: AsyncSession = Depends(get_db), redis=Depends(get_redis), current_user=Depends(get_current_user)):
    service = TaskService(db, redis)
    tasks = await service.list_tasks(project_id, page, page_size, status, priority, assignee_id, sort_by, order)
    return tasks


@router.get("/tasks/{task_id}", response_model=TaskResponse)
async def get_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db), redis=Depends(get_redis), current_user=Depends(get_current_user)):
    service = TaskService(db, redis)
    task = await service.get_task_by_id(task_id)
    return task


@router.patch("/tasks/{task_id}", response_model=TaskResponse)
async def update_task(data: TaskUpdate, task_id: uuid.UUID, db: AsyncSession = Depends(get_db), redis=Depends(get_redis), current_user=Depends(get_current_user)):
    service = TaskService(db, redis)
    task = await service.update_task(task_id, data, current_user.id)
    return task


@router.patch("/tasks/{task_id}/status", response_model=TaskResponse)
async def update_status(data: TaskStatusUpdate, task_id: uuid.UUID, db: AsyncSession = Depends(get_db), redis=Depends(get_redis), current_user=Depends(get_current_user)):
    service = TaskService(db, redis)
    task = await service.update_status(task_id, data, current_user.id)
    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: uuid.UUID, db: AsyncSession = Depends(get_db), redis=Depends(get_redis), current_user=Depends(get_current_user)):
    service = TaskService(db, redis)
    result = await service.delete_task(task_id, current_user.id)
    return result