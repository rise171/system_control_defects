from typing import List, Optional
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.settings import get_session
from app.repository.user_repos import UserRepos
from app.schemas.user import UserCreate, UserUpdate, UserGetting

class UserService:

    @staticmethod
    async def get_all_users(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[UserGetting]:
        try:
            return await UserRepos.get_all_users(limit=limit, offset=offset, session=session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get users: {str(e)}")

    @staticmethod
    async def get_user_by_id(user_id: int, session: AsyncSession = Depends(get_session)) -> UserGetting:
        user = await UserRepos.get_user_by_id(user_id, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def create_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserGetting:
        try:
            return await UserRepos.create_user(user_data, session)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

    @staticmethod
    async def update_user(user_id: int, user_data: UserUpdate, session: AsyncSession = Depends(get_session)) -> UserGetting:
        user = await UserRepos.update_user(user_id, user_data, session)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)) -> dict:
        success = await UserRepos.delete_user(user_id, session)
        if not success:
            raise HTTPException(status_code=404, detail="User not found")
        return {"message": "User deleted successfully"}