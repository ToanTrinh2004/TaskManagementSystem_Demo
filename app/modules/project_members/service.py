from app.modules.project_members.repository import ProjectMemberRepository
from sqlalchemy.ext.asyncio import AsyncSession

class ProjectMemberService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.member_repo = ProjectMemberRepository(db)