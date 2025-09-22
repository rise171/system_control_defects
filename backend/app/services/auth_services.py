from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.settings import get_session
from app.repository.auth_repos import AuthRepos
from app.schemas.user import UserCreate, UserGetting, LoginRequest
from app.core.security import create_jwt_token
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from datetime import timedelta

class AuthService:

    @staticmethod
    async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)) -> UserGetting:
        try:
            user = await AuthRepos.register_user(
                email=user_data.email,
                password=user_data.password,
                name=user_data.name,
                role=user_data.role,
                session=session
            )
            return UserGetting.model_validate(user)
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to register user: {str(e)}")

    @staticmethod
    async def login_user(login_data: LoginRequest, session: AsyncSession = Depends(get_session)) -> dict:
        try:
            user = await AuthRepos.authenticate_user(
                email=login_data.email,
                password=login_data.password,
                session=session
            )
            if not user:
                raise HTTPException(status_code=401, detail="Invalid credentials")
            
            # Создаем токен
            access_token = create_jwt_token(
                data={"sub": str(user.id), "user_id": user.id, "email": user.email, "role": user.role},
                expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": UserGetting.model_validate(user)
            }
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to login: {str(e)}")