"""Likes apps schemas."""
from datetime import datetime

from pydantic import Field
from typing_extensions import Annotated

from apps.common.schemas import BaseInSchema


class CreateLikeIn(BaseInSchema):
    """Like creation in schema, for creation not admin user."""

    eval: Annotated[bool, Field(examples=[False], description='Like evaluation')]
    post_id: Annotated[int, Field(examples=[1], description='Post id to evaluate')]


class AdminCreateLikeIn(CreateLikeIn):
    """Like creation in schema for admin user."""

    user_id: Annotated[
        int,
        Field(examples=[1], description='Like created by user with id'),
    ]


class AdminPartiallyUpdateLikeIn(BaseInSchema):
    """Admin partially update in schema."""

    eval: bool | None = None
    post_id: int | None = None
    user_id: int | None = None


class CreateLikeOut(BaseInSchema):
    """Like creation out schema, created not admin user."""

    id: Annotated[int, Field(description='Like id', examples=[1])]
    eval: Annotated[bool, Field(description='Like evaluation', examples=[False])]
    created_at: Annotated[datetime, Field(description='Like created at')]
    user_id: Annotated[
        int,
        Field(description='Like created user with id', examples=[1]),
    ]
    post_id: Annotated[
        int,
        Field(description='Like created to post with id', examples=[2]),
    ]
