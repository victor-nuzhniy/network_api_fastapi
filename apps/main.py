"""Main FastAPI module."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.common.exceptions import BackendError
from apps.common.exceptions_handlers import backend_error_handler
from settings import Settings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.CORS_ALLOW_ORIGINS,
    allow_credentials=Settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=Settings.CORS_ALLOW_METHODS,
    allow_headers=Settings.CORS_ALLOW_HEADERS,
)


app.add_exception_handler(BackendError, backend_error_handler)  # type: ignore
