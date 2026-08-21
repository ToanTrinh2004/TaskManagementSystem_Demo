from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel

from app.modules.tasks.model import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]= None
    priority: TaskPriority 
    assignee_id: Optional[uuid.UUID]= None
    due_date: Optional[datetime]= None
    estimated_finish_date: Optional[datetime] = None


class TaskResponse(BaseModel):
    id: uuid.UUID
    title: str
    description: Optional[str]
    project_id: uuid.UUID
    status: TaskStatus
    priority: TaskPriority
    assignee_id: Optional[uuid.UUID]
    assigned_by: Optional[uuid.UUID]
    created_by: uuid.UUID
    due_date: Optional[datetime]
    estimated_finish_date: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    assignee_id: Optional[uuid.UUID] = None
    due_date: Optional[datetime] = None

class TaskStatusUpdate(BaseModel):
    status: TaskStatus