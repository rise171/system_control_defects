from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database.settings import get_session
from app.models.attachment import DefectAttachment
from app.schemas.attachment import DefectAttachmentCreate, DefectAttachmentUpdate, DefectAttachmentGetting

class DefectAttachmentRepos:

    @classmethod
    async def get_all_attachments(cls, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[DefectAttachmentGetting]:
        query = select(DefectAttachment).offset(offset).limit(limit)
        result = await session.execute(query)
        attachments = result.scalars().all()
        return [DefectAttachmentGetting.model_validate(attachment) for attachment in attachments]

    @classmethod
    async def get_attachment_by_id(cls, attachment_id: int, session: AsyncSession = Depends(get_session)) -> Optional[DefectAttachmentGetting]:
        query = select(DefectAttachment).filter(DefectAttachment.id == attachment_id)
        result = await session.execute(query)
        attachment = result.scalar_one_or_none()
        if not attachment:
            return None
        return DefectAttachmentGetting.model_validate(attachment)

    @classmethod
    async def create_attachment(cls, attachment_data: DefectAttachmentCreate, session: AsyncSession = Depends(get_session)) -> DefectAttachmentGetting:
        new_attachment = DefectAttachment(**attachment_data.model_dump())
        session.add(new_attachment)
        await session.commit()
        await session.refresh(new_attachment)
        return DefectAttachmentGetting.model_validate(new_attachment)

    @classmethod
    async def update_attachment(cls, attachment_id: int, attachment_data: DefectAttachmentUpdate, session: AsyncSession = Depends(get_session)) -> Optional[DefectAttachmentGetting]:
        query = select(DefectAttachment).filter(DefectAttachment.id == attachment_id)
        result = await session.execute(query)
        attachment = result.scalar_one_or_none()
        
        if not attachment:
            return None
        
        update_data = attachment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(attachment, field, value)
        
        await session.commit()
        await session.refresh(attachment)
        return DefectAttachmentGetting.model_validate(attachment)

    @classmethod
    async def delete_attachment(cls, attachment_id: int, session: AsyncSession = Depends(get_session)) -> bool:
        query = select(DefectAttachment).filter(DefectAttachment.id == attachment_id)
        result = await session.execute(query)
        attachment = result.scalar_one_or_none()
        
        if not attachment:
            return False
        
        await session.delete(attachment)
        await session.commit()
        return True

    @classmethod
    async def get_attachments_by_defect(cls, defect_id: int, session: AsyncSession = Depends(get_session)) -> List[DefectAttachmentGetting]:
        query = select(DefectAttachment).filter(DefectAttachment.defect_id == defect_id)
        result = await session.execute(query)
        attachments = result.scalars().all()
        return [DefectAttachmentGetting.model_validate(attachment) for attachment in attachments]