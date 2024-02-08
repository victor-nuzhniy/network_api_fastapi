"""Common project utilities."""
from datetime import datetime

from pytz import utc
from sqlalchemy import DATETIME, TypeDecorator
from typing_extensions import Type

TIME = Type[datetime]


class AwareDateTime(TypeDecorator):
    """Results returned as aware datetimes, not naive ones."""

    impl = DATETIME

    @property
    def python_type(
        self,
    ) -> Type[datetime]:
        """Get python type."""
        return datetime

    def process_bind_param(self, dt_value: datetime, dialect: str) -> datetime:
        """Process bind parameter."""
        if dt_value is not None:
            if not dt_value.tzinfo:
                raise TypeError('tzinfo is required')
            dt_value = dt_value.astimezone(utc).replace(tzinfo=None)
        return dt_value

    def process_literal_param(self, dt_value: datetime, dialect: str) -> None:
        """Process literal parameter."""

    def process_result_value(self, dt_value: datetime, dialect: str) -> datetime:
        """Process result value."""
        return dt_value.replace(tzinfo=utc)
