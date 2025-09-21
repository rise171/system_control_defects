from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.settings import get_session
from app.repository.comment_repos import CommentRepos
from app.schemas.comment import CommentCreate, CommentUpdate, CommentGetting

class CommentService:

    @staticmethod
    async def get_all_comments(limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[CommentGetting]:
        try:
            return await CommentRepos.get_all_comments(limit=limit, offset=offset, session=session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get comments: {str(e)}")

    @staticmethod
    async def get_comment_by_id(comment_id: int, session: AsyncSession = Depends(get_session)) -> CommentGetting:
        comment = await CommentRepos.get_comment_by_id(comment_id, session)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    @staticmethod
    async def create_comment(comment_data: CommentCreate, session: AsyncSession = Depends(get_session)) -> CommentGetting:
        try:
            return await CommentRepos.create_comment(comment_data, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to create comment: {str(e)}")

    @staticmethod
    async def update_comment(comment_id: int, comment_data: CommentUpdate, session: AsyncSession = Depends(get_session)) -> CommentGetting:
        comment = await CommentRepos.update_comment(comment_id, comment_data, session)
        if not comment:
            raise HTTPException(status_code=404, detail="Comment not found")
        return comment

    @staticmethod
    async def delete_comment(comment_id: int, session: AsyncSession = Depends(get_session)) -> dict:
        success = await CommentRepos.delete_comment(comment_id, session)
        if not success:
            raise HTTPException(status_code=404, detail="Comment not found")
        return {"message": "Comment deleted successfully"}

    @staticmethod
    async def get_comments_by_defect(defect_id: int, session: AsyncSession = Depends(get_session)) -> List[CommentGetting]:
        try:
            return await CommentRepos.get_comments_by_defect(defect_id, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get defect comments: {str(e)}")

    @staticmethod
    async def get_comments_by_author(author_id: int, session: AsyncSession = Depends(get_session)) -> List[CommentGetting]:
        try:
            return await CommentRepos.get_comments_by_author(author_id, session)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to get user comments: {str(e)}")