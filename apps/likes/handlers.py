"""Likes apps handlers."""
from fastapi import Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Sequence

from apps.common.exceptions import BackendError
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
        if created_like is None:
            raise BackendError(message="Like haven't been created.")
        if isinstance(created_like, Sequence):
            raise BackendError(
                message='Improper executor call',
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return CreateLikeOut(
            id=created_like.id,
            eval=created_like.eval,
            created_at=created_like.created_at,
            user_id=created_like.user_id,
            post_id=created_like.post_id,
        )


like_handlers = LikeHandlers()
