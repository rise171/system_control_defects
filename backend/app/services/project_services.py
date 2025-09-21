from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.settings import get_session
from app.repository.project_repos import ProjectRepos
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectGetting

class ProjectService:

    @staticmethod
    async def get_all_projects(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[ProjectGetting]:
        try:
            return await ProjectRepos.get_all_projects(limit=limit, offset=offset, session=session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get projects: {str(e)}")

    @staticmethod
    async def get_project_by_id(project_id: int, session: AsyncSession = Depends(get_session)) -> ProjectGetting:
        project = await ProjectRepos.get_project_by_id(project_id, session)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    @staticmethod
    async def create_project(project_data: ProjectCreate, session: AsyncSession = Depends(get_session)) -> ProjectGetting:
        try:
            return await ProjectRepos.create_project(project_data, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")

    @staticmethod
    async def update_project(project_id: int, project_data: ProjectUpdate, session: AsyncSession = Depends(get_session)) -> ProjectGetting:
        project = await ProjectRepos.update_project(project_id, project_data, session)
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    @staticmethod
    async def delete_project(project_id: int, session: AsyncSession = Depends(get_session)) -> dict:
        success = await ProjectRepos.delete_project(project_id, session)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")
        return {"message": "Project deleted successfully"}