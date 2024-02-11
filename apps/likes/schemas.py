"""Likes apps schemas."""
from datetime import datetime

from pydantic import Field
from typing_extensions import Annotated

from apps.common.schemas import BaseInSchema


class CreateLikeIn(BaseInSchema):
    """Like creation in schema, for creation not admin user."""

    eval: Annotated[bool, Field(examples=[False], description='Like evaluation')]
    post_id: Annotated[int, Field(examples=[1], description='Post id to evaluate')]


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
