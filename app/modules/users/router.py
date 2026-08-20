from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
import uuid
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.dependencies import get_current_user
from app.db.redis_client import get_redis
from app.db.session import get_db
from app.modules.users.schemas import LoginRequest, LoginResponse, RefreshRequest, RefreshTokenResponse, UserCreate, UserResponse
from app.modules.users.service import UserService



bearer_scheme = HTTPBearer()
router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db),  redis_client=Depends(get_redis)):
    service = UserService(db, redis_client)
    new_user = await service.create_user(user_data)
    return new_user

@router.get("/{id}", response_model=UserResponse)
async def get_user(id: uuid.UUID, db: AsyncSession = Depends(get_db),  redis_client=Depends(get_redis)):
    service = UserService(db, redis_client)
    user = await service.get_user(id)
    return user
    
@router.post("/login", response_model= LoginResponse)
async def login(data : LoginRequest, db: AsyncSession = Depends(get_db), redis_client=Depends(get_redis)):
    service = UserService(db, redis_client)
    result = await service.login(data.email,data.password)
    return result
   
      
    
@router.post("/refresh",response_model= RefreshTokenResponse)
async def refresh(data: RefreshRequest, db: AsyncSession = Depends(get_db), redis_client=Depends(get_redis),credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    service = UserService(db, redis_client)
    access_token = credentials.credentials
    result = await service.refresh(data.refresh_token,access_token)
    return result
    
@router.post("/logout")
async def logout(db: AsyncSession = Depends(get_db),redis_client=Depends(get_redis),current_user = Depends(get_current_user)):
    service = UserService(db, redis_client)
    await service.logout(current_user.id)
    return {"message": "Logout successful"}

