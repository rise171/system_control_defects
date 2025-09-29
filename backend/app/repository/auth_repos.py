from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException

from app.database.settings import get_session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_jwt_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from app.models.user import UserRole

from app.core.security import create_jwt_token as create_access_token

class AuthRepos:
    @staticmethod
    async def register_user(email: str, name: str, password: str, role: UserRole, session: AsyncSession):
        existing_user = await session.execute(select(User).filter(User.email == email))
        if existing_user.scalar():
            return None

        hashed_password = hash_password(password)

        new_user = User(
            email=email, 
            name=name,  
            password_hash=hashed_password,
            role=role  
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user.id

    @staticmethod
    async def authenticate_user(email: str, password: str, session: AsyncSession):
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    async def login_user(email: str, password: str, session: AsyncSession):
        user = await AuthRepos.authenticate_user(email, password, session)
        if not user:
            return None

        access_token = create_access_token(data={"sub": str(user.id)})
        return {
            "access_token": access_token,
            "user_id": user.id,
            "role": user.role
        }