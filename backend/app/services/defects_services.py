from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.settings import get_session
from app.repository.defect_repos import DefectRepos
from app.schemas.defect import DefectCreate, DefectUpdate, DefectGetting

class DefectService:

    @staticmethod
    async def get_all_defects(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[DefectGetting]:
        try:
            return await DefectRepos.get_all_defects(limit=limit, offset=offset, session=session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get defects: {str(e)}")

    @staticmethod
    async def get_defect_by_id(defect_id: int, session: AsyncSession = Depends(get_session)) -> DefectGetting:
        defect = await DefectRepos.get_defect_by_id(defect_id, session)
        if not defect:
            raise HTTPException(status_code=404, detail="Defect not found")
        return defect

    @staticmethod
    async def create_defect(defect_data: DefectCreate, session: AsyncSession = Depends(get_session)) -> DefectGetting:
        try:
            return await DefectRepos.create_defect(defect_data, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create defect: {str(e)}")

    @staticmethod
    async def update_defect(defect_id: int, defect_data: DefectUpdate, session: AsyncSession = Depends(get_session)) -> DefectGetting:
        defect = await DefectRepos.update_defect(defect_id, defect_data, session)
        if not defect:
            raise HTTPException(status_code=404, detail="Defect not found")
        return defect

    @staticmethod
    async def delete_defect(defect_id: int, session: AsyncSession = Depends(get_session)) -> dict:
        success = await DefectRepos.delete_defect(defect_id, session)
        if not success:
            raise HTTPException(status_code=404, detail="Defect not found")
        return {"message": "Defect deleted successfully"}

    @staticmethod
    async def get_defects_by_project(project_id: int, session: AsyncSession = Depends(get_session)) -> List[DefectGetting]:
        try:
            return await DefectRepos.get_defects_by_project(project_id, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get project defects: {str(e)}")

    @staticmethod
    async def get_defects_by_assignee(user_id: int, session: AsyncSession = Depends(get_session)) -> List[DefectGetting]:
        try:
            return await DefectRepos.get_defects_by_assignee(user_id, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get user defects: {str(e)}")