import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
    async def create_user(self, data: UserCreate) -> User:
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise ValueError("Email already exits")
        hashed_password =  pwd_context.hash(data.password)
        user = User(
            email=data.email,
            full_name=data.full_name,
            password=hashed_password,
        )
        return await self.repo.create(user)
    
    async def get_user(self, user_id: uuid.UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user