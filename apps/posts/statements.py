"""Posts apps query statements."""
from apps.common.base_statements import BaseCRUDStatements
from apps.posts.models import Like, Post

post_crud_statements = BaseCRUDStatements(model=Post)
like_crud_statements = BaseCRUDStatements(model=Like)
