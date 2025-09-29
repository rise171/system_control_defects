from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import LoginRequest
from pydantic import BaseModel, EmailStr
from app.database.settings import get_session
from app.services.auth_services import AuthService
from app.schemas.user import UserCreate, UserGetting
from app.core.security import get_current_user

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

@auth_router.post("/login", response_model=dict)
async def login_user(data: LoginRequest, session: AsyncSession = Depends(get_session)):
    return await AuthService.login_user(data.email, data.password, session)

@auth_router.post("/register", response_model=UserGetting)
async def register_user(user_data: UserCreate, session: AsyncSession = Depends(get_session)):
    user_id = await AuthService.register_user(user_data, session)
    if not user_id:
        raise HTTPException(status_code=400, detail="User already exists")

    user = await AuthService.get_user_profile(user_id, session)
    if not user:
        raise HTTPException(status_code=404, detail="User Not Found")

    return user

@auth_router.get("/me", response_model=UserGetting)
async def get_current_user_info(
    current_user: UserGetting = Depends(get_current_user)
):
    return current_user