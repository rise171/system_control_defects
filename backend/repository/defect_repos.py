from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database.settings import get_session
from app.models.defects import Defect
from app.schemas.defect import DefectCreate, DefectUpdate, DefectGetting

class DefectRepos:

    @classmethod
    async def get_all_defects(cls, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[DefectGetting]:
        query = select(Defect).offset(offset).limit(limit)
        result = await session.execute(query)
        defects = result.scalars().all()
        return [DefectGetting.model_validate(defect) for defect in defects]

    @classmethod
    async def get_defect_by_id(cls, defect_id: int, session: AsyncSession = Depends(get_session)) -> Optional[DefectGetting]:
        query = select(Defect).filter(Defect.id == defect_id)
        result = await session.execute(query)
        defect = result.scalar_one_or_none()
        if not defect:
            return None
        return DefectGetting.model_validate(defect)

    @classmethod
    async def create_defect(cls, defect_data: DefectCreate, session: AsyncSession = Depends(get_session)) -> DefectGetting:
        new_defect = Defect(**defect_data.model_dump())
        session.add(new_defect)
        await session.commit()
        await session.refresh(new_defect)
        return DefectGetting.model_validate(new_defect)

    @classmethod
    async def update_defect(cls, defect_id: int, defect_data: DefectUpdate, session: AsyncSession = Depends(get_session)) -> Optional[DefectGetting]:
        query = select(Defect).filter(Defect.id == defect_id)
        result = await session.execute(query)
        defect = result.scalar_one_or_none()
        
        if not defect:
            return None
        
        update_data = defect_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(defect, field, value)
        
        await session.commit()
        await session.refresh(defect)
        return DefectGetting.model_validate(defect)

    @classmethod
    async def delete_defect(cls, defect_id: int, session: AsyncSession = Depends(get_session)) -> bool:
        query = select(Defect).filter(Defect.id == defect_id)
        result = await session.execute(query)
        defect = result.scalar_one_or_none()
        
        if not defect:
            return False
        
        await session.delete(defect)
        await session.commit()
        return True

    @classmethod
    async def get_defects_by_project(cls, project_id: int, session: AsyncSession = Depends(get_session)) -> List[DefectGetting]:
        query = select(Defect).filter(Defect.project_id == project_id)
        result = await session.execute(query)
        defects = result.scalars().all()
        return [DefectGetting.model_validate(defect) for defect in defects]

    @classmethod
    async def get_defects_by_assignee(cls, user_id: int, session: AsyncSession = Depends(get_session)) -> List[DefectGetting]:
        query = select(Defect).filter(Defect.assigned_to_id == user_id)
        result = await session.execute(query)
        defects = result.scalars().all()
        return [DefectGetting.model_validate(defect) for defect in defects]