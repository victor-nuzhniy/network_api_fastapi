"""Posts apps routers."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from apps.common.base_routers import BaseRouterInitializer
from apps.common.dependencies import get_async_session
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.common.user_dependencies import get_current_user
from apps.posts.handlers import post_handlers
from apps.posts.models import Post
from apps.posts.schemas import (
    AdminCreatePostIn,
    AdminPartiallyUpdatePostIn,
    CreatePostIn,
    CreatePostOut,
)
from apps.user.models import User

posts_router = APIRouter()


admin_post_router_initializer = BaseRouterInitializer(  # type: ignore
    router=posts_router,
    in_schemas=(AdminCreatePostIn, AdminCreatePostIn, AdminPartiallyUpdatePostIn),
    out_schema=CreatePostOut,
    model=Post,
)

admin_post_router_initializer.initialize_routers()


@posts_router.post(
    '/post/',
    name='create_post',
    response_model=JSENDOutSchema[CreatePostOut],
    summary='Create post',
    responses={
        200: {'description': 'Successful create post response'},
        422: {'model': JSENDFailOutSchema, 'description': 'ValidationError'},
    },
    tags=['Posts application'],
)
async def create_post(
    request: Request,
    post: Annotated[CreatePostIn, Depends()],
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
