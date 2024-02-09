"""User apps schemas."""
from datetime import datetime

from pydantic import Field, model_validator

from apps.common.constants import EMAIL_REGEX
from apps.common.schemas import BaseInSchema, BaseOutSchema


class CreateUserIn(BaseInSchema):
    """User creation in schema."""

    username: str = Field(max_length=50)
    email: str = Field(max_length=100, pattern=EMAIL_REGEX)
    password: str = Field(max_length=120)
    password_re_check: str

    @model_validator(mode='after')
    def re_check_password(self) -> 'CreateUserIn':
        """Check whether password_re_check is equal to password."""
        password = self.password
        r_password = self.password_re_check
        if password is not None and r_password is not None and password != r_password:
            raise ValueError("Password don't match!")
        return self


class CreateUserOut(BaseOutSchema):
    """User creation out schema."""

    user_id: int
    username: str
    last_visit_at: datetime
    email: str
    is_active: bool
