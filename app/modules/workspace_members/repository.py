import uuid
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.workspace_members.model import WorkSpaceMember

class WorkSpaceMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_member(self, member: WorkSpaceMember):
        self.db.add(member)
        await self.db.flush()
        return member

    async def get_member(self, workspace_id: uuid.UUID, user_id: uuid.UUID):
        query = select(WorkSpaceMember).where(
            WorkSpaceMember.workspace_id == workspace_id,
            WorkSpaceMember.user_id == user_id,
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()
    
    async def list_members(self, workspace_id: uuid.UUID):
        query = select(WorkSpaceMember).where(WorkSpaceMember.workspace_id == workspace_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete_all_by_workspace(self, workspace_id):
        query = delete(WorkSpaceMember).where(WorkSpaceMember.workspace_id == workspace_id)
        await self.db.execute(query)
        await self.db.commit()
    
    async def delete_member(self, member: WorkSpaceMember):
        await self.db.delete(member)
        await self.db.commit()

    async def update_member(self, member: WorkSpaceMember):
        await self.db.add(member)
        await self.db.commit()
        await self.db.refresh(member)
        return member
    
