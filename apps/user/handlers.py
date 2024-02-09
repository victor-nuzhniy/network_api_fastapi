"""User apps handlers."""
from fastapi import Request
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.exceptions import BackendError
from apps.common.orm_services import statement_executor
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
        statement: str = user_crud_statements.create_statement(
            schema=user,
            obj_data={'is_active': True},
        )
        created_user: Row = await statement_executor.execute_statement(
            session,
            statement,
        )
        if created_user is None:
            raise BackendError(message="User haven't been created.")
        return CreateUserOut(**created_user._asdict())  # noqa: WPS437


user_handlers = UserHandlers()