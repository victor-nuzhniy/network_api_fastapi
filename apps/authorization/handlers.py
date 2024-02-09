"""Authorization apps handlers."""
from fastapi import Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from apps.authorization.auth_utilities import (
    create_access_token,
    create_refresh_token,
    verify_password,
    verify_user,
)
from apps.authorization.schemas import AuthOut
from apps.common.orm_services import statement_executor
from apps.user.statements import user_crud_statements


class AuthorizationHandlers(object):
    """Handlers for authorization apps."""

    async def login(
        self,
        *,
        request: Request,
        form_data: OAuth2PasswordRequestForm,
        session: AsyncSession,
    ) -> AuthOut:
        """Login user with given credentials."""
        statement: str = user_crud_statements.read_statement(
            obj_data={'login': form_data.username},
        )
        user: Row = await statement_executor.execute_statement(session, statement)
        verify_user(user)
        verify_password(user, form_data.password)
        return AuthOut(
            access_token=create_access_token(user.email),
            refresh_token=create_refresh_token(user.email),
            id=user.id,
        )


authorization_handlers = AuthorizationHandlers()
