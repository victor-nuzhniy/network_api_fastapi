"""Posts apps handlers."""
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Sequence

from apps.common.common_utilities import checkers
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
        checked_post: Post = checkers.check_created_instance(created_post, 'Post')
        return CreatePostOut.model_validate(checked_post)


post_handlers = PostHandlers()
