import uuid
import redis
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


from app.core.sercurity import create_access_token, create_refresh_token, decode_token
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession,redis_client: redis.Redis):
        self.repo = UserRepository(db)
        self.redis = redis_client

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
        return await self.repo.create_user(user)
    
    async def get_user(self, user_id: uuid.UUID) -> User:
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise ValueError("User not found")
        return user
    

    async def login(self, email, password):
        ## check user exist by email
        user_data = await self.repo.get_by_email(email)
        if not user_data:
            raise ValueError("sai email hoac password")
        
        ## compare to hash_password in db 
        check = pwd_context.verify(password, user_data.password)
        if check == False:
            raise ValueError("sai email hoac password")
        
        ## generate access_token and refresh_token
        acess_token = create_access_token(str(user_data.id))
        refresh_token = create_refresh_token(str(user_data.id))
        
        ## saved refresh token in redis using set { user_id : refresh_token} in order to manage session
        await self.redis.set(f"refresh_token:{user_data.id}", refresh_token, ex=60*60*24*7)
        
        return {"access_token": acess_token, 
                "refresh_token" : refresh_token,
                "token_type": "bearer"}
    
    async def refresh(self,refresh_token):
        payload = decode_token(refresh_token)
        
        ## check type of token
        if payload.get("type") != "refresh":
            raise ValueError("Refresh token không hợp lệ")
        
        ## get user_id from payload
        user_id = payload.get("sub")
       
        ## get refresh_token was stored in redis 
        saved_token = await self.redis.get(f"refresh_token:{user_id}")

        if saved_token != refresh_token:
            raise ValueError("Refresh token không hợp lệ")
        
        ## create and return new access_token
        access_token = create_access_token(user_id)
        return {
        "access_token": access_token,
        "token_type": "bearer"}
    
    async def logout(self, user_id):
        ## remove refresh token from redis to revoke the session
        await self.redis.delete(f"refresh_token:{user_id}")