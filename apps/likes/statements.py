"""Likes apps statements."""
from apps.common.base_statements import BaseCRUDStatements
from apps.likes.models import Like

like_crud_statements = BaseCRUDStatements(model=Like)
