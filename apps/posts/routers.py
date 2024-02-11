"""Posts apps routers."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from apps.common.dependencies import get_async_session
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.common.user_dependencies import get_current_user
from apps.posts.handlers import post_handlers
from apps.posts.schemas import CreatePostIn, CreatePostOut
from apps.user.models import User

posts_router = APIRouter()


@posts_router.post(
    '/post/',
    name='create_post',
    response_model=JSENDOutSchema[CreatePostOut],
    summary='Create post',
    responses={
        200: {'description': 'Successful create user response'},
        422: {'model': JSENDFailOutSchema, 'description': 'ValidationError'},
    },
    tags=['Posts application'],
)
async def create_post(
    request: Request,
    post: CreatePostIn,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict:
    """Create post router."""
    created_post: CreatePostOut = await post_handlers.create_post(
        request,
        post,
        user,
        session,
    )
    return {
        'data': created_post,
        'message': 'Created post with id {id}'.format(id=created_post.id),
    }
