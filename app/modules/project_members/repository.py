import uuid

from sqlalchemy import select
from app.modules.project_members.model import ProjectMember
from sqlalchemy.ext.asyncio import AsyncSession

class ProjectMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_member(self, member: ProjectMember):
        await self.db.add(member)
        await self.db.flush()
        return member
    
    async def list_member(self,project_id:uuid.UUID):
        query = select(ProjectMember).where(ProjectMember.project_id == project_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_project_member_by_id(self,user_id : uuid.UUID,project_id:uuid.UUID):
        query = select(ProjectMember).where(ProjectMember.user_id == user_id,ProjectMember.project_id == project_id)
        result  =  await self.db.execute(query)
        return result.scalars().one_or_none()
