from asyncio import Task
import json
from typing import Optional
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
import redis
from app.core.exceptions import ForbiddenError, NotFoundError
from app.modules.project_members.model import ProjectRole
from app.modules.project_members.repository import ProjectMemberRepository
from app.modules.projects.repository import ProjectRepository
from app.modules.tasks.model import TaskStatus
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schemas import TaskCreate, TaskUpdate
from app.core.config import settings


class TaskService:
    def __init__(self, db: AsyncSession, redis_client=None):
        self.db = db
        self.redis = redis
        self.repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.project_member_repo =ProjectMemberRepository(db)
## helper func
    async def __check_exits_project(self, project_id: uuid.UUID):
        project = await self.project_repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        return project
    
    async def __check_is_project_member(self, project_id: uuid.UUID, user_id: uuid.UUID):
        member = await self.project_member_repo.get_project_member_by_id(user_id, project_id)
        if not member:
            raise ForbiddenError("You are not a member of this project")
        return member
    
    async def __check_exits_task(self, task_id: uuid.UUID):
        task = await self.repo.get_task_by_id(task_id)
        if not task:
            raise NotFoundError("Task not found")
        return task
    
    async def __clear_task_cache(self, project_id: uuid.UUID):
    
        pattern = f"tasks_cache:{project_id}:*"
        
        async for key in self.redis.scan_iter(match=pattern):
            await self.redis.delete(key)


## main func
    async def create_task(self, project_id: uuid.UUID, data: TaskCreate, user_id: uuid.UUID):
        await self.__check_exits_project(project_id)
        member = await self.__check_is_project_member(project_id, user_id)
        if member.role == ProjectRole.MEMBER:
            raise ForbiddenError("You have no rights")

        new_task = Task(
            title=data.title ,
            description = data.description,
            project_id = project_id,
            priority= data.priority,
            assignee_id = data.assignee_id,
            assigned_by=user_id ,
            created_by=user_id ,
            due_date=data.due_date,
            estimated_finish_date=data.estimated_finish_date,
            status=TaskStatus.NOT_START,
        )
        task = await self.repo.create_task(new_task)

        return task
    

    async def list_tasks(
        self,
        project_id: uuid.UUID,
        page: int = 1,
        page_size: int = 20,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        assignee_id: Optional[uuid.UUID] = None,
        sort_by: str = "created_at",
        order: str = "desc",
    ):

        await self.__check_exits_project(project_id)

        ## create cache key
        cache_key = (
            f"tasks_cache:"
            f"{project_id}:"
            f"{page}:"
            f"{page_size}:"
            f"{status}:"
            f"{priority}:"
            f"{assignee_id}:"
            f"{sort_by}:"
            f"{order}"
        )
        print(cache_key)
        ## check in redis if cached then load from it no need query db
        cached = await self.redis.get(cache_key)
        if cached:
            return json.loads(cached)

        items, total = await self.repo.list_tasks(
            project_id=project_id,
            page=page,
            page_size=page_size,
            status=status,
            priority=priority,
            assignee_id=assignee_id,
            sort_by=sort_by,
            order=order,
        )
        ## if not cached , build a json to store in redis
        result = {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": [
                {
                    "id": str(t.id),
                    "title": t.title,
                    "description": t.description,
                    "project_id": str(t.project_id),
                    "status": t.status,
                    "priority": t.priority,
                    "assignee_id": str(t.assignee_id) if t.assignee_id else None,
                    "assigned_by": str(t.assigned_by) if t.assigned_by else None,
                    "created_by": str(t.created_by),
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                    "estimated_finish_date": t.estimated_finish_date.isoformat() if t.estimated_finish_date else None,
                    "created_at": t.created_at.isoformat(),
                    "updated_at": t.updated_at.isoformat(),
                }
                for t in items
            ],
        }

        if self.redis:
            await self.redis.set(cache_key, json.dumps(result), ex=settings.TASK_CACHE_TTL)

        return result
    
    async def get_task_by_id(self, task_id: uuid.UUID):
        return await self.__check_exits_task(task_id)
    

    async def update_task(self, task_id: uuid.UUID, data:TaskUpdate, user_id:uuid.UUID):
        task = await self.__check_exits_task(task_id)
        await self.__check_is_project_member(task.project_id, user_id)

        if data.title is not None:
            task.title = data.title
        if data.description is not None:
            task.description = data.description
        if data.priority is not None:
            task.priority = data.priority
        if data.assignee_id is not None:
            ## check is new member receive task is project member
            await self.__check_is_project_member(task.project_id, data.assignee_id)
            task.assignee_id = data.assignee_id
            task.assigned_by = user_id
        if data.due_date is not None:
            task.due_date = data.due_date

        updated = await self.repo.update_task(task)

        self.__clear_task_cache(task.project_id)
        

        return updated


