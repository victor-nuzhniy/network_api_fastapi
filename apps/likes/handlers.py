"""Likes apps handlers."""
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Sequence

from apps.common.common_utilities import checkers
from apps.common.orm_services import statement_executor as executor
from apps.likes.models import Like
from apps.likes.schemas import CreateLikeIn, CreateLikeOut
from apps.likes.statements import like_crud_statements
from apps.user.models import User


class LikeHandlers(object):
    """Like handlers."""

    async def create_like(
        self,
        request: Request,
        like: CreateLikeIn,
        user: User,
        session: AsyncSession,
    ) -> CreateLikeOut:
        """Create like."""
        statement: str = like_crud_statements.create_statement(
            schema=like,
            obj_data={'user_id': user.id},
        )
        created_like: Like | Sequence[
            Like | None
        ] | None = await executor.execute_statement(
            session,
            statement,
            commit=True,
        )
        checked_like: Like = checkers.check_created_instance(created_like, 'Like')
        return CreateLikeOut(
            id=checked_like.id,
            eval=checked_like.eval,
            created_at=checked_like.created_at,
            user_id=checked_like.user_id,
            post_id=checked_like.post_id,
        )


like_handlers = LikeHandlers()
