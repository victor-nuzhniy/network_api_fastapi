"""User specific dependencies."""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.engine import Row
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Annotated

from apps.common.common_utilities import get_token_data
from apps.common.dependencies import get_async_session
from apps.common.exceptions import BackendError
from apps.common.orm_services import statement_executor
from apps.user.statements import user_crud_statements

reusable_oauth = OAuth2PasswordBearer(tokenUrl='/login', scheme_name='JWT')


async def get_current_user(
    token: Annotated[str, Depends(reusable_oauth)],
    session: Annotated[AsyncSession, Depends(get_async_session)],
) -> Row:
    """Get current user, using token."""
    try:
        token_data = get_token_data(token)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Credential verification failed',
            headers={'WWW-Authenticate': 'Bearer'},
        )
    read_user_stmt = user_crud_statements.read_statement(
        obj_data={'email': token_data.sub},
    )
    user: Row | None = await statement_executor.execute_statement(
        session,
        read_user_stmt,
    )
    if user is None:
        raise BackendError(
            message='User not found',
            code=status.HTTP_404_NOT_FOUND,
        )
    return user
