"""Schemas for posts apps."""
from datetime import datetime

from pydantic import Field
from typing_extensions import Annotated

from apps.common.schemas import BaseInSchema, BaseOutSchema


class CreatePostIn(BaseInSchema):
    """Post creation in schema."""

    message: Annotated[
        str,
        Field(description='Post message', max_length=255, min_length=1),
    ]


class CreatePostOut(BaseOutSchema):
    """Post creation out schema."""

    id: Annotated[int, Field(description='Post id')]
    message: Annotated[str, Field(description='Post message')]
    created_at: Annotated[datetime, Field(description='Post created at')]
    updated_at: Annotated[datetime, Field(description='Post updated at')]
    user_id: Annotated[int, Field(description='Post created user id')]
