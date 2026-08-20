from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.db.session import get_db
from app.modules.users.schemas import LoginRequest, LoginResponse, UserCreate, UserResponse
from app.modules.users.service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse)
async def create_user(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        new_user = await service.create_user(user_data)
        return new_user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{id}", response_model=UserResponse)
async def get_user(id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        user = await service.get_user(id)
        return user
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.post("/login", response_model= LoginResponse)
async def login(data : LoginRequest, db: AsyncSession = Depends(get_db)):
    service = UserService(db)
    try:
        result = await service.login(data.email,data.password)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))