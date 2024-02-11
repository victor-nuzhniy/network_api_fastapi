"""Schemas for posts apps."""
from pydantic import Field
from typing_extensions import Annotated

from apps.common.common_utilities import AwareDateTime
from apps.common.schemas import BaseInSchema, BaseOutSchema


class CreatePostIn(BaseInSchema):
    """Post creation in schema."""

    message: Annotated[str, Field(title='Post message', max_length=255, min_length=1)]


class CreatePostOut(BaseOutSchema):
    """Post creation out schema."""

    id: Annotated[int, Field(title='Post id')]
    message: Annotated[str, Field(title='Post message')]
    created_at: Annotated[AwareDateTime, Field(title='Post created at')]
    updated_at: Annotated[AwareDateTime, Field(title='Post updated at')]
    user_id: Annotated[int, Field(title='Post created user id')]
