from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.settings import get_session
from app.services.project_services import ProjectService
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectGetting
from app.core.security import get_current_user

p_router = APIRouter(prefix="/projects", tags=["Projects"])

@p_router.get("/", response_model=List[ProjectGetting])
async def get_all_projects(
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await ProjectService.get_all_projects(limit, offset, session)

@p_router.get("/{project_id}", response_model=ProjectGetting)
async def get_project_by_id(
    project_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await ProjectService.get_project_by_id(project_id, session)

@p_router.post("/", response_model=ProjectGetting, status_code=status.HTTP_201_CREATED)
async def create_project(
    project_data: ProjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await ProjectService.create_project(project_data, session)

@p_router.put("/{project_id}", response_model=ProjectGetting)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await ProjectService.update_project(project_id, project_data, session)

@p_router.delete("/{project_id}", status_code=status.HTTP_200_OK)
async def delete_project(
    project_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await ProjectService.delete_project(project_id, session)