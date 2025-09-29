from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.settings import get_session
from app.repository.auth_repos import AuthRepos
from app.schemas.user import UserCreate, UserGetting, LoginRequest
from app.core.security import create_jwt_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta
from sqlalchemy.future import select
from app.models.user import User

class AuthService:
    @staticmethod
    async def register_user(user_data: UserCreate, session: AsyncSession) -> int:
        user_id = await AuthRepos.register_user(
            user_data.email, 
            user_data.name,  
            user_data.password, 
            user_data.role,
            session
        )
        if not user_id:
            return None
        user = await AuthService.get_user_profile(user_id, session)
        if not user:
            raise HTTPException(status_code=404)
        return user.id

    @staticmethod
    async def get_user_profile(user_id: int, session: AsyncSession = Depends(get_session)):
        result = await session.execute(select(User).filter(User.id == user_id))
        user = result.scalar()
        return user

    @staticmethod
    async def login_user(email: str, password: str, session: AsyncSession):
        # Убрали Depends(get_session) по умолчанию
        token = await AuthRepos.login_user(email, password, session)
        if not token:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        return {"access_token": token, "token_type": "bearer"}