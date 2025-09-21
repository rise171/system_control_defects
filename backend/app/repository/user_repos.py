from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException

from app.database.settings import get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserGetting
from app.core.security import hash_password

class UserRepos:

    @classmethod
    async def get_all_users(cls, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[UserGetting]:
        query = select(User).offset(offset).limit(limit)
        result = await session.execute(query)
        users = result.scalars().all()
        return [UserGetting.model_validate(user) for user in users]

    @classmethod
    async def get_user_by_id(cls, user_id: int, session: AsyncSession = Depends(get_session)) -> Optional[UserGetting]:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        if not user:
            return None
        return UserGetting.model_validate(user)

    @classmethod
    async def create_user(cls, user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserGetting:
        existing_user = await session.execute(select(User).filter(User.email == user_data.email))
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User with this email already exists")
        
        hashed_password = hash_password(user_data.password)
        new_user = User(
            email=user_data.email,
            password_hash=hashed_password,
            name=user_data.name,
            role=user_data.role
        )
        
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return UserGetting.model_validate(new_user)

    @classmethod
    async def update_user(cls, user_id: int, user_data: UserUpdate, session: AsyncSession = Depends(get_session)) -> Optional[UserGetting]:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return None
        
        update_data = user_data.model_dump(exclude_unset=True)
        
        if 'password' in update_data:
            update_data['password_hash'] = hash_password(update_data.pop('password'))
        
        for field, value in update_data.items():
            setattr(user, field, value)
        
        await session.commit()
        await session.refresh(user)
        return UserGetting.model_validate(user)

    @classmethod
    async def delete_user(cls, user_id: int, session: AsyncSession = Depends(get_session)) -> bool:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        
        if not user:
            return False
        
        await session.delete(user)
        await session.commit()
        return True