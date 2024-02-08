"""Project SQLAlchemy orm services."""
from sqlalchemy.engine import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from typing_extensions import Sequence, TypeVar

from apps.common.db import Base

ModelType = TypeVar('ModelType', bound=Base)


class StatementExecutor(object):
    """Async CRUD operations."""

    async def execute_statement(
        self,
        session: AsyncSession,
        statement: str,
        commit: bool = False,
        many: bool = False,
    ) -> ModelType | Sequence[ModelType] | None:
        """Execute statement."""
        alchemy_result: ChunkedIteratorResult = await session.execute(statement)
        if commit:
            await session.commit()
        if many:
            return alchemy_result.scalars().all()
        return alchemy_result.scalar_one_or_none()


statement_executor = StatementExecutor()
