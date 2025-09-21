from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from app.database.settings import get_session
from app.models.comment import Comment
from app.schemas.comment import CommentCreate, CommentUpdate, CommentGetting

class CommentRepos:

    @classmethod
    async def get_all_comments(cls, limit: int = 100, offset: int = 0, session: AsyncSession = Depends(get_session)) -> List[CommentGetting]:
        query = select(Comment).offset(offset).limit(limit)
        result = await session.execute(query)
        comments = result.scalars().all()
        return [CommentGetting.model_validate(comment) for comment in comments]

    @classmethod
    async def get_comment_by_id(cls, comment_id: int, session: AsyncSession = Depends(get_session)) -> Optional[CommentGetting]:
        query = select(Comment).filter(Comment.id == comment_id)
        result = await session.execute(query)
        comment = result.scalar_one_or_none()
        if not comment:
            return None
        return CommentGetting.model_validate(comment)

    @classmethod
    async def create_comment(cls, comment_data: CommentCreate, session: AsyncSession = Depends(get_session)) -> CommentGetting:
        new_comment = Comment(**comment_data.model_dump())
        session.add(new_comment)
        await session.commit()
        await session.refresh(new_comment)
        return CommentGetting.model_validate(new_comment)

    @classmethod
    async def update_comment(cls, comment_id: int, comment_data: CommentUpdate, session: AsyncSession = Depends(get_session)) -> Optional[CommentGetting]:
        query = select(Comment).filter(Comment.id == comment_id)
        result = await session.execute(query)
        comment = result.scalar_one_or_none()
        
        if not comment:
            return None
        
        update_data = comment_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(comment, field, value)
        
        await session.commit()
        await session.refresh(comment)
        return CommentGetting.model_validate(comment)

    @classmethod
    async def delete_comment(cls, comment_id: int, session: AsyncSession = Depends(get_session)) -> bool:
        query = select(Comment).filter(Comment.id == comment_id)
        result = await session.execute(query)
        comment = result.scalar_one_or_none()
        
        if not comment:
            return False
        
        await session.delete(comment)
        await session.commit()
        return True

    @classmethod
    async def get_comments_by_defect(cls, defect_id: int, session: AsyncSession = Depends(get_session)) -> List[CommentGetting]:
        query = select(Comment).filter(Comment.defect_id == defect_id)
        result = await session.execute(query)
        comments = result.scalars().all()
        return [CommentGetting.model_validate(comment) for comment in comments]

    @classmethod
    async def get_comments_by_author(cls, author_id: int, session: AsyncSession = Depends(get_session)) -> List[CommentGetting]:
        query = select(Comment).filter(Comment.author_id == author_id)
        result = await session.execute(query)
        comments = result.scalars().all()
        return [CommentGetting.model_validate(comment) for comment in comments]