from asyncio import Task
import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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