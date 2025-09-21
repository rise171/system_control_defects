from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import Depends, HTTPException

from app.database.settings import get_session
from app.models.user import User
from app.core.security import hash_password, verify_password, create_jwt_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

class AuthRepos:

    @staticmethod
    async def register_user(email: str, password: str, name: str, role: str, session: AsyncSession = Depends(get_session)):
        # Проверяем, существует ли пользователь
        existing_user = await session.execute(select(User).filter(User.email == email))
        if existing_user.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="User with this email already exists")

        hashed_password = hash_password(password)
        new_user = User(email=email, password_hash=hashed_password, name=name, role=role)
        
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

    @staticmethod
    async def authenticate_user(email: str, password: str, session: AsyncSession = Depends(get_session)):
        result = await session.execute(select(User).filter(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.password_hash):
            return None
        return user

    @staticmethod
    async def login_user(email: str, password: str, session: AsyncSession = Depends(get_session)):
        user = await AuthRepos.authenticate_user(email, password, session)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Создаем JWT токен с помощью функции из security
        access_token = create_jwt_token(
            data={"sub": str(user.id), "user_id": user.id, "email": user.email, "role": user.role},
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }

    @staticmethod
    async def get_current_user_from_token(token: str, session: AsyncSession = Depends(get_session)):
        from app.core.security import decode_jwt_token
        
        payload = decode_jwt_token(token)
        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        user_id = payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        # Получаем пользователя из базы
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user