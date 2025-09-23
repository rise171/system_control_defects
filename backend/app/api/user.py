from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.settings import get_session
from app.services.user_services import UserService
from app.schemas.user import UserCreate, UserUpdate, UserGetting
from app.core.security import get_current_user

user_router = APIRouter(prefix="/users", tags=["Users"])

@user_router.get("/", response_model=List[UserGetting])
async def get_all_users(
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user: UserGetting = Depends(get_current_user)
):
    return await UserService.get_all_users(limit, offset, session)

@user_router.get("/{user_id}", response_model=UserGetting)
async def get_user_by_id(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserGetting = Depends(get_current_user)
):
    return await UserService.get_user_by_id(user_id, session)

@user_router.post("/", response_model=UserGetting, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session),
    current_user: UserGetting = Depends(get_current_user)
):
    return await UserService.create_user(user_data, session)

@user_router.put("/{user_id}", response_model=UserGetting)
async def update_user(
    user_id: int,
    user_data: UserUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: UserGetting = Depends(get_current_user)
):
    return await UserService.update_user(user_id, user_data, session)

@user_router.delete("/{user_id}", status_code=status.HTTP_200_OK)
async def delete_user(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: UserGetting = Depends(get_current_user)
):
    return await UserService.delete_user(user_id, session)