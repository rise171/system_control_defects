from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.settings import get_session
from app.services.attachment_services import DefectAttachmentService
from app.schemas.attachment import DefectAttachmentCreate, DefectAttachmentUpdate, DefectAttachmentGetting
from app.core.security import get_current_user

a_router = APIRouter(prefix="/attachments", tags=["Attachments"])

@a_router.get("/", response_model=List[DefectAttachmentGetting])
async def get_all_attachments(
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectAttachmentService.get_all_attachments(limit, offset, session)

@a_router.get("/{attachment_id}", response_model=DefectAttachmentGetting)
async def get_attachment_by_id(
    attachment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectAttachmentService.get_attachment_by_id(attachment_id, session)

@a_router.get("/defect/{defect_id}", response_model=List[DefectAttachmentGetting])
async def get_attachments_by_defect(
    defect_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectAttachmentService.get_attachments_by_defect(defect_id, session)

@a_router.post("/", response_model=DefectAttachmentGetting, status_code=status.HTTP_201_CREATED)
async def create_attachment(
    attachment_data: DefectAttachmentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectAttachmentService.create_attachment(attachment_data, session)

@a_router.put("/{attachment_id}", response_model=DefectAttachmentGetting)
async def update_attachment(
    attachment_id: int,
    attachment_data: DefectAttachmentUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectAttachmentService.update_attachment(attachment_id, attachment_data, session)

@a_router.delete("/{attachment_id}", status_code=status.HTTP_200_OK)
async def delete_attachment(
    attachment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await DefectAttachmentService.delete_attachment(attachment_id, session)