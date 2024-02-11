"""Posts apps handlers."""
from fastapi import Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Sequence

from apps.common.exceptions import BackendError
from apps.common.orm_services import statement_executor as executor
from apps.posts.models import Post
from apps.posts.schemas import CreatePostIn, CreatePostOut
from apps.posts.statements import post_crud_statements
from apps.user.models import User


class PostHandlers(object):
    """Post handlers."""

    async def create_post(
        self,
        request: Request,
        post: CreatePostIn,
        user: User,
        session: AsyncSession,
    ) -> CreatePostOut:
        """Create post."""
        statement: str = post_crud_statements.create_statement(
            schema=post,
            obj_data={'user_id': user.id},
        )
        created_post: Post | Sequence[
            Post | None
        ] | None = await executor.execute_statement(
            session,
            statement,
            commit=True,
        )
        if created_post is None:
            raise BackendError(message="Post haven't been created.")
        if isinstance(created_post, Sequence):
            raise BackendError(
                message='Improper executor call',
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return CreatePostOut(
            id=created_post.id,
            message=created_post.message,
            created_at=created_post.created_at,
            updated_at=created_post.updated_at,
            user_id=created_post.user_id,
        )


post_handlers = PostHandlers()
