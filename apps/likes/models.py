"""Models for likes apps."""
from sqlalchemy import Boolean, Column, ForeignKey, Integer, func
from sqlalchemy.orm import relationship

from apps.common.common_utilities import AwareDateTime
from apps.common.db import Base


class Like(Base):
    """Like model."""

    __tablename__ = 'like'

    id = Column(Integer, primary_key=True, nullable=False)
    eval = Column(Boolean, default=False, nullable=False)
    created_at = Column(AwareDateTime, default=func.now(), nullable=False)
    user_id = Column(
        Integer,
        ForeignKey('user.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    post_id = Column(
        Integer,
        ForeignKey('post.id', ondelete='CASCADE', onupdate='CASCADE'),
        nullable=False,
    )
    user = relationship('User', back_populates='likes')
    post = relationship('Post', back_populates='likes')

    def __repr__(self) -> str:
        """Represent class instance."""
        return ''.join(
            (
                '{name}(id={id}, eval={eval}, created_at={created_at}, '.format(
                    name=self.__class__.__name__,
                    id=self.id,
                    eval=self.eval,
                    created_at=self.created_at,
                ),
                'user_id={user_id}, post_id={post_id})'.format(
                    user_id=self.user_id,
                    post_id=self.post_id,
                ),
            ),
        )
