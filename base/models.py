from sqlalchemy import Boolean, Column, DateTime, Integer
from sqlalchemy.sql import func

from apps.database import Base


class BaseModel(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    deleted_at = Column(
        DateTime(timezone=True),
        nullable=True,
    )

    is_deleted = Column(
        Boolean,
        default=False,
        nullable=False,
    )

    created_by = Column(
        Integer,
        nullable=True,
    )

    updated_by = Column(
        Integer,
        nullable=True,
    )
