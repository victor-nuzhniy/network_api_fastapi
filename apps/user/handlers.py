"""User apps handlers."""
from fastapi import Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Sequence

from apps.authorization.auth_utilities import get_hashed_password
from apps.common.exceptions import BackendError
from apps.common.orm_services import statement_executor as executor
from apps.user.models import User
from apps.user.schemas import CreateUserIn, CreateUserOut
from apps.user.statements import user_crud_statements


class UserHandlers(object):
    """User handlers."""

    async def create_user(
        self,
        request: Request,
        user: CreateUserIn,
        session: AsyncSession,
    ) -> CreateUserOut:
        """Create user with given data."""
        hashed_password = get_hashed_password(user.password)
        statement: str = user_crud_statements.create_statement(
            obj_data={
                'username': user.username,
                'email': user.email,
                'password': hashed_password,
                'is_active': True,
            },
        )
        created_user: User | Sequence[
            User | None
        ] | None = await executor.execute_statement(
            session,
            statement,
            commit=True,
        )
        if created_user is None:
            raise BackendError(message="User haven't been created.")
        if isinstance(created_user, Sequence):
            raise BackendError(
                message='Improper executor call',
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return CreateUserOut(
            id=created_user.id,
            username=created_user.username,
            email=created_user.email,
            is_active=created_user.is_active,
        )


user_handlers = UserHandlers()
