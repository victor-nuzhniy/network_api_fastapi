"""Common project types."""
from pydantic import BaseModel
from typing_extensions import TypeVar

from apps.common.db import Base

ModelType = TypeVar('ModelType', bound=Base)
SchemaType = TypeVar('SchemaType', bound=BaseModel)


class LocalSchema(BaseModel):
    """Class for type checking."""

    id: int
