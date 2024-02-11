"""Models for posts apps."""
from sqlalchemy import Column, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship

from apps.common.common_utilities import AwareDateTime
from apps.common.db import Base


class Post(Base):
    """Post model."""

    __tablename__ = 'post'

    id = Column(Integer, primary_key=True, nullable=False)
    message = Column(String(255), nullable=False)
    created_at = Column(AwareDateTime, default=func.now(), nullable=False)
    updated_at = Column(
        AwareDateTime,
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    user = relationship('User', back_populates='posts')
    likes = relationship('Like', back_populates='post')

    def __repr__(self) -> str:
        """Represent model instance."""
        return ''.join(
            (
                '{name}(id={id}, created_at={created_at}, '.format(
                    name=self.__class__.__name__,
                    id=self.id,
                    created_at=self.created_at,
                ),
                'updated_at={updated_at}, user_id={user_id})'.format(
                    updated_at=self.updated_at,
                    user_id=self.user_id,
                ),
            ),
        )
