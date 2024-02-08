"""Statements for db data manipulation for user apps."""
from apps.common.base_statements import AsyncBaseCRUDStatements
from apps.user.models import User

user_crud_statements = AsyncBaseCRUDStatements(model=User)
