from asyncio import Task
from typing import Optional
import uuid
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.tasks.model import TaskPriority, TaskStatus

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task:Task):
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_task_by_id(self, task_id : uuid.UUID):
        query = select(Task).where(Task.id == task_id)
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def list_tasks(
        self,
        project_id: uuid.UUID,
        page: int,
        page_size: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        assignee_id: Optional[uuid.UUID] = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ):
        
        query = select(Task).where(Task.project_id ==project_id)

        # Filter 
        if status:
            query= query.where(Task.status == status)
        if priority:
            query= query.where(Task.priority == priority)
        if assignee_id:
            query = query.where(Task.assignee_id == assignee_id)


        # Sort
        if sort_by == "due_date":
            sort_column= Task.due_date
        else:
            sort_column= Task.created_at
            
        if order == "asc":
            query = query.order_by(sort_column.asc())
        else:
            query = query.order_by(sort_column.desc())

        # Pagination
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)
        result = await self.db.execute(query)
        tasks = result.scalars().all()

        # Count total 
        count_query = select(func.count()).select_from(Task).where(Task.project_id ==project_id)
        
        if status:
            count_query = count_query.where(Task.status == status)

        if priority:
            count_query = count_query.where(Task.priority == priority)

        if assignee_id:
            count_query = count_query.where(Task.assignee_id == assignee_id)

        total = (await self.db.execute(count_query)).scalar()

        return tasks, total
    
    async def update_task(self, task: Task) -> Task:
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task: Task):
        await self.db.delete(task)
        await self.db.commit()