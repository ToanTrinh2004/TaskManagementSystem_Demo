from datetime import datetime
from typing import Optional
import uuid

from pydantic import BaseModel

from app.modules.tasks.model import TaskPriority


class TaskCreate(BaseModel):
    title: str
    description: Optional[str]= None
    priority: TaskPriority 
    assignee_id: Optional[uuid.UUID]= None
    due_date: Optional[datetime]= None
    estimated_finish_date: Optional[datetime] = None