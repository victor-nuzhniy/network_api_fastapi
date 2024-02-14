"""Likes apps routers."""
from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from apps.common.base_routers import BaseRouterInitializer
from apps.common.dependencies import get_async_session
from apps.common.schemas import JSENDFailOutSchema, JSENDOutSchema
from apps.common.user_dependencies import get_current_user
from apps.likes.handlers import like_handlers
from apps.likes.models import Like
from apps.likes.schemas import AdminCreateLikeIn, CreateLikeIn, CreateLikeOut
from apps.user.models import User

likes_router = APIRouter()


admin_like_router_initializer = BaseRouterInitializer(  # type: ignore
    router=likes_router,
    in_schema=AdminCreateLikeIn,
    out_schema=CreateLikeOut,
    model=Like,
)

admin_like_router_initializer.initialize_routers()


@likes_router.post(
    '/like/',
    name='create_like',
    response_model=JSENDOutSchema[CreateLikeOut],
    summary='Create like',
    responses={
        200: {'description': 'Successful create like response'},
        422: {'model': JSENDFailOutSchema, 'description': 'ValidationError'},
    },
    tags=['Likes application'],
)
async def create_like(
    request: Request,
    like: Annotated[CreateLikeIn, Depends()],
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> dict:
    """Create post router."""
    created_like: CreateLikeOut = await like_handlers.create_like(
        request,
        like,
        user,
        session,
    )
    return {
        'data': created_like,
        'message': 'Created like with id {id}'.format(id=created_like.id),
    }
