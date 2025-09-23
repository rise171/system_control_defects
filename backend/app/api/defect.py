from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.settings import get_session
from app.services.defects_services import DefectService
from app.schemas.defect import DefectCreate, DefectUpdate, DefectGetting
from app.core.security import get_current_user

d_router = APIRouter(prefix="/defects", tags=["Defects"])

@d_router.get("/", response_model=List[DefectGetting])
async def get_all_defects(
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectService.get_all_defects(limit, offset, session)

@d_router.get("/{defect_id}", response_model=DefectGetting)
async def get_defect_by_id(
    defect_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectService.get_defect_by_id(defect_id, session)

@d_router.get("/project/{project_id}", response_model=List[DefectGetting])
async def get_defects_by_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectService.get_defects_by_project(project_id, session)

@d_router.get("/user/{user_id}", response_model=List[DefectGetting])
async def get_defects_by_assignee(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectService.get_defects_by_assignee(user_id, session)

@d_router.post("/", response_model=DefectGetting, status_code=status.HTTP_201_CREATED)
async def create_defect(
    defect_data: DefectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectService.create_defect(defect_data, session)

@d_router.put("/{defect_id}", response_model=DefectGetting)
async def update_defect(
    defect_id: int,
    defect_data: DefectUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectService.update_defect(defect_id, defect_data, session)

@d_router.delete("/{defect_id}", status_code=status.HTTP_200_OK)
async def delete_defect(
    defect_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectService.delete_defect(defect_id, session)