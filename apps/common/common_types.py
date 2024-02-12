"""Common project types."""
from __future__ import annotations

from pydantic import BaseModel
from typing_extensions import Any, Protocol, TypeVar

from apps.common.db import Base

ModelType = TypeVar('ModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel, covariant=True)


class LocalSchema(Protocol[SchemaType]):
    """Class for type checking."""

    id: int

    @classmethod
    def model_validate(cls, *args: Any, **kwargs: Any) -> SchemaType:
        """Validate model."""
