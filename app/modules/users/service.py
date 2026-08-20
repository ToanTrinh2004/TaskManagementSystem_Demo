import uuid
import redis.asyncio as redis
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext


from app.core.sercurity import create_access_token, create_refresh_token, decode_token
from app.core.exceptions import NotFoundError, UnauthorizedError, BadRequestError
from app.modules.users.model import User
from app.modules.users.repository import UserRepository
from app.modules.users.schemas import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    def __init__(self, db: AsyncSession,redis_client: redis.Redis):
        self.repo = UserRepository(db)
        self.redis = redis_client

    async def create_user(self, data: UserCreate):
        existing = await self.repo.get_by_email(data.email)
        if existing:
            raise BadRequestError("Email already exits")
        hashed_password =  pwd_context.hash(data.password)
        user = User(
            email=data.email,
            full_name=data.full_name,
            password=hashed_password,
        )
        return await self.repo.create_user(user)
    
    async def get_user(self, user_id: uuid.UUID) :
        user = await self.repo.get_by_id(user_id)
        if not user:
            raise NotFoundError("User not found")
        return user
    

    async def login(self, email, password):
        ## check user exist by email
        user_data = await self.repo.get_by_email(email)
        if not user_data:
            raise UnauthorizedError("Invalid email or password")
        
        ## hash and compare to password in db 
        check = pwd_context.verify(password, user_data.password)
        if check == False:
            raise UnauthorizedError("Invalid email or password")
        
        ## generate access_token and refresh_token
        acess_token = create_access_token(str(user_data.id))
        refresh_token = create_refresh_token(str(user_data.id))
        
        ## saved refresh token in redis using set { user_id : refresh_token} in order to manage session
        await self.redis.set(f"refresh_token:{user_data.id}", refresh_token, ex=60*60*24*7)
        
        return {"access_token": acess_token, 
                "refresh_token" : refresh_token,
                "token_type": "bearer"}
    
    async def refresh(self,refresh_token,access_token):
        payload = decode_token(refresh_token)
        
        ## check type of token
        if payload.get("type") != "refresh":
            raise UnauthorizedError("Refresh token không hợp lệ")
        
        user_id = payload.get("sub")
       
        ## get refresh_token was stored in redis 
        saved_token = await self.redis.get(f"refresh_token:{user_id}")

        if saved_token != refresh_token:
            raise UnauthorizedError("Refresh token không hợp lệ")
        ## remove old refresh
        await self.redis.delete(f"refresh_token:{user_id}")
        ## create and return new access_token and refreshtoken
        new_access_token = create_access_token(user_id)
        new_refresh_token = create_refresh_token(user_id)
        ## save new refresh token to redis
        await self.redis.set(f"refresh_token:{user_id}", new_refresh_token, ex=60*60*24*7)
        ## create blaclist for access_token
        await self.redis.set(f"blacklist:{access_token}", "1", ex=60*30)
       
        return {
        "access_token": new_access_token,
        "refresh_token" : new_refresh_token,
        "token_type": "bearer"}
    
    async def logout(self, user_id):
        ## remove refresh token from redis to revoke the session
        await self.redis.delete(f"refresh_token:{user_id}")