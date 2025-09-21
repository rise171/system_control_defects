from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database.settings import get_session
from app.models.project import Project
from app.schemas.projects import ProjectCreate, ProjectUpdate, ProjectGetting

class ProjectRepos:

    @classmethod
    async def get_all_projects(cls, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[ProjectGetting]:
        query = select(Project).offset(offset).limit(limit)
        result = await session.execute(query)
        projects = result.scalars().all()
        return [ProjectGetting.model_validate(project) for project in projects]

    @classmethod
    async def get_project_by_id(cls, project_id: int, session: AsyncSession = Depends(get_session)) -> Optional[ProjectGetting]:
        query = select(Project).filter(Project.id == project_id)
        result = await session.execute(query)
        project = result.scalar_one_or_none()
        if not project:
            return None
        return ProjectGetting.model_validate(project)

    @classmethod
    async def create_project(cls, project_data: ProjectCreate, session: AsyncSession = Depends(get_session)) -> ProjectGetting:
        new_project = Project(**project_data.model_dump())
        session.add(new_project)
        await session.commit()
        await session.refresh(new_project)
        return ProjectGetting.model_validate(new_project)

    @classmethod
    async def update_project(cls, project_id: int, project_data: ProjectUpdate, session: AsyncSession = Depends(get_session)) -> Optional[ProjectGetting]:
        query = select(Project).filter(Project.id == project_id)
        result = await session.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            return None
        
        update_data = project_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(project, field, value)
        
        await session.commit()
        await session.refresh(project)
        return ProjectGetting.model_validate(project)

    @classmethod
    async def delete_project(cls, project_id: int, session: AsyncSession = Depends(get_session)) -> bool:
        query = select(Project).filter(Project.id == project_id)
        result = await session.execute(query)
        project = result.scalar_one_or_none()
        
        if not project:
            return False
        
        await session.delete(project)
        await session.commit()
        return True