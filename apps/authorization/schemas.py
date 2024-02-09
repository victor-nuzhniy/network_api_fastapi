"""Authorization schemas."""
from datetime import datetime

from apps.common.schemas import BaseInSchema, BaseOutSchema


class TokenPayload(BaseInSchema):
    """Token payload schema."""

    exp: int
    sub: str


class UserOut(BaseOutSchema):
    """User out schema."""

    id: int
    username: str
    email: str
    is_active: bool = False
    is_admin: bool = False
    last_visit_at: datetime
    created_at: datetime
    updated_at: datetime


class UserIn(TokenPayload):
    """User in schema."""

    id: int


class AuthOut(BaseOutSchema):
    """Authorization out schema."""

    access_token: str
    refresh_token: str
    id: int
