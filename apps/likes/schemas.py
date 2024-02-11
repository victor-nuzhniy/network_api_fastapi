"""Likes apps schemas."""
from datetime import datetime

from pydantic import Field
from typing_extensions import Annotated

from apps.common.schemas import BaseInSchema


class CreateLikeIn(BaseInSchema):
    """Like creation in schema."""

    eval: Annotated[bool, Field(title='Like evaluation', default=False)]
    post_id: Annotated[int, Field(title='Post id to evaluate', default=1)]


class CreateLikeOut(BaseInSchema):
    """Like creation out schema."""

    id: Annotated[int, Field(title='Like id', examples=[1])]
    eval: Annotated[bool, Field(title='Like evaluation', examples=[False])]
    created_at: Annotated[datetime, Field(title='Like created at')]
    user_id: Annotated[int, Field(title='Like created user with id')]
    post_id: Annotated[int, Field(title='Like created to post with id')]
