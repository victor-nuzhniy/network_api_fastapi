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
        ] | None = await executor.execute_return_statement(
            session,
            statement,
            commit=True,
        )
        checked_like: Like = checkers.check_created_instance(created_like, 'Like')
        return CreateLikeOut.model_validate(checked_like)


like_handlers = LikeHandlers()
