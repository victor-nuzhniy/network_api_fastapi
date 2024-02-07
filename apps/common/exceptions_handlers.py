"""App exceptions handlers."""
from fastapi import Request, status
from fastapi.responses import JSONResponse, Response
from sqlalchemy.exc import IntegrityError

from apps.common.enum import JSENDStatus
from apps.common.exceptions import BackendError
from settings import Settings


def backend_error_handler(request: Request, exc: BackendError) -> Response:
    """Return result from Back-end exception."""
    return JSONResponse(content=exc.dict(), status_code=exc.code)


def integrity_error_handler(error: IntegrityError) -> None:
    """Raise error from IntegrityError."""
    if 'duplicate' in error.args[0]:
        error_message = error.orig.args[0].split('\n')[-1]
        raise BackendError(
            message=str(error_message) if Settings.DEBUG else 'Update error.',
        )
    else:
        raise BackendError(  # noqa: WPS503
            message=str(error) if Settings.DEBUG else 'Internal server error.',
            code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            status=JSENDStatus.ERROR,
        )
