from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.settings import get_session
from app.repository.attachement_repos import DefectAttachmentRepos
from app.schemas.attachment import DefectAttachmentCreate, DefectAttachmentUpdate, DefectAttachmentGetting

class DefectAttachmentService:

    @staticmethod
    async def get_all_attachments(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[DefectAttachmentGetting]:
        try:
            return await DefectAttachmentRepos.get_all_attachments(limit=limit, offset=offset, session=session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get attachments: {str(e)}")

    @staticmethod
    async def get_attachment_by_id(attachment_id: int, session: AsyncSession = Depends(get_session)) -> DefectAttachmentGetting:
        attachment = await DefectAttachmentRepos.get_attachment_by_id(attachment_id, session)
        if not attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        return attachment

    @staticmethod
    async def create_attachment(attachment_data: DefectAttachmentCreate, session: AsyncSession = Depends(get_session)) -> DefectAttachmentGetting:
        try:
            return await DefectAttachmentRepos.create_attachment(attachment_data, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create attachment: {str(e)}")

    @staticmethod
    async def update_attachment(attachment_id: int, attachment_data: DefectAttachmentUpdate, session: AsyncSession = Depends(get_session)) -> DefectAttachmentGetting:
        attachment = await DefectAttachmentRepos.update_attachment(attachment_id, attachment_data, session)
        if not attachment:
            raise HTTPException(status_code=404, detail="Attachment not found")
        return attachment

    @staticmethod
    async def delete_attachment(attachment_id: int, session: AsyncSession = Depends(get_session)) -> dict:
        success = await DefectAttachmentRepos.delete_attachment(attachment_id, session)
        if not success:
            raise HTTPException(status_code=404, detail="Attachment not found")
        return {"message": "Attachment deleted successfully"}

    @staticmethod
    async def get_attachments_by_defect(defect_id: int, session: AsyncSession = Depends(get_session)) -> List[DefectAttachmentGetting]:
        try:
            return await DefectAttachmentRepos.get_attachments_by_defect(defect_id, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get defect attachments: {str(e)}")