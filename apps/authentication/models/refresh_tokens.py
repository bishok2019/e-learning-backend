from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
    text,
)

from apps.database import Base


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )
    token = Column(
        Text,
        unique=True,
        nullable=False,
    )
    expires_at = Column(
        DateTime,
        nullable=False,
    )
    is_blacklisted = Column(
        Boolean,
        nullable=False,
        default=False,
        server_default=text("false"),
    )
