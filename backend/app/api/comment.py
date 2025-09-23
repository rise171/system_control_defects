from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database.settings import get_session
from app.services.comment_services import CommentService
from app.schemas.comment import CommentCreate, CommentUpdate, CommentGetting
from app.core.security import get_current_user

c_router = APIRouter(prefix="/comments", tags=["Comments"])

@c_router.get("/", response_model=List[CommentGetting])
async def get_all_comments(
    limit: int = 100,
    offset: int = 0,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await CommentService.get_all_comments(limit, offset, session)

@c_router.get("/{comment_id}", response_model=CommentGetting)
async def get_comment_by_id(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await CommentService.get_comment_by_id(comment_id, session)

@c_router.get("/defect/{defect_id}", response_model=List[CommentGetting])
async def get_comments_by_defect(
    defect_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await CommentService.get_comments_by_defect(defect_id, session)

@c_router.get("/user/{user_id}", response_model=List[CommentGetting])
async def get_comments_by_author(
    user_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await CommentService.get_comments_by_author(user_id, session)

@c_router.post("/", response_model=CommentGetting, status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await CommentService.create_comment(comment_data, session)

@c_router.put("/{comment_id}", response_model=CommentGetting)
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await CommentService.update_comment(comment_id, comment_data, session)

@c_router.delete("/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(
    comment_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: dict = Depends(get_current_user)
):
    return await CommentService.delete_comment(comment_id, session)