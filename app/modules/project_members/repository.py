class ProjectMemberRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_member(self, member: ProjectMember):
        self.db.add(member)
        await self.db.flush()
        return member