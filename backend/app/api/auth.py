from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import LoginRequest
from app.database.settings import get_session
from app.services.auth_services import AuthService
from app.schemas.user import UserCreate, UserGetting
from app.core.security import get_current_user

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserGetting, status_code=status.HTTP_201_CREATED)
async def register_user(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_session)
):
    return await AuthService.register_user(user_data, session)

@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_session)
):
    
    login_data = LoginRequest(email=form_data.username, password=form_data.password)
    return await AuthService.login_user(login_data, session)

@router.get("/me", response_model=UserGetting)
async def get_current_user_info(
    current_user: UserGetting = Depends(get_current_user)
):
    return current_user