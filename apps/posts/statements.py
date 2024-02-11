"""Posts apps query statements."""
from apps.common.base_statements import BaseCRUDStatements
from apps.posts.models import Post

post_crud_statements = BaseCRUDStatements(model=Post)
