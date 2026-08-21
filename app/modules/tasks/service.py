from asyncio import Task
from typing import Optional
import uuid
from app.core.exceptions import ForbiddenError, NotFoundError
from app.modules.project_members.model import ProjectRole
from app.modules.project_members.repository import ProjectMemberRepository
from app.modules.projects.repository import ProjectRepository
from app.modules.tasks.model import TaskStatus
from app.modules.tasks.repository import TaskRepository
from app.modules.tasks.schemas import TaskCreate


class TaskService:
    def __init__(self, db: AsyncSession, redis_client=None):
        self.db = db
        self.repo = TaskRepository(db)
        self.project_repo = ProjectRepository(db)
        self.project_member_repo =ProjectMemberRepository(db)


    async def create_task(self, project_id: uuid.UUID, data: TaskCreate, user_id: uuid.UUID):
        project = await self.project_repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")
        member = await self.project_member_repo.get_project_member_by_id(user_id, project_id)
        if not member:
            raise ForbiddenError("You are not a member of this project")
        if member.role == ProjectRole.MEMBER:
            raise 

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

        project = await self.project_repo.get_project_by_id(project_id)
        if not project:
            raise NotFoundError("Project not found")

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

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items,
        }

