"""Main FastAPI module."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from apps.authorization.routers import authorization_router
from apps.common.exceptions import BackendError
from apps.common.exceptions_handlers import backend_error_handler
from apps.likes.routers import likes_router
from apps.posts.routers import posts_router
from apps.user.routers import users_router
from settings import Settings
from tags_metadata import metadata

app = FastAPI(openapi_tags=metadata)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.CORS_ALLOW_ORIGINS,
    allow_credentials=Settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=Settings.CORS_ALLOW_METHODS,
    allow_headers=Settings.CORS_ALLOW_HEADERS,
)


app.add_exception_handler(BackendError, backend_error_handler)  # type: ignore

app.include_router(users_router)
app.include_router(authorization_router)
app.include_router(posts_router)
app.include_router(likes_router)
