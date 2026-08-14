import enum

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
)
from sqlalchemy.orm import relationship

from apps.database import Base
from base.models import BaseModel


class UserType(enum.Enum):
    STUDENT = "STUDENT"
    SYSTEM = "SYSTEM"
    TEACHER = "TEACHER"


class CustomUser(BaseModel):
    __tablename__ = "users"
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    user_type = Column(Enum(UserType), default=UserType.SYSTEM, nullable=False)

    # user_notifications = relationship(
    #     "UserNotification", back_populates="user"
    # )  # reverse relationship to UserNotification
    user_roles = relationship(
        "CustomRole", secondary="user_roles", back_populates="users"
    )  # reverse relationship to UserRole
    user_permissions = relationship(
        "CustomPermission", secondary="user_permissions", back_populates="users"
    )  # reverse relationship to UserPermission


# Association tables for many-to-many relationships
user_roles = Table(
    "user_roles",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    ),
    extend_existing=True,  # This allows us to redefine the table if it already exists, which can be useful during development
)
# Association tables for many-to-many relationships
user_permissions = Table(
    "user_permissions",
    Base.metadata,
    Column(
        "user_id", Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    extend_existing=True,  # This allows us to redefine the table if it already exists, which can be useful during development
)
# Association table for many-to-many relationship between roles and permissions
role_permissions = Table(
    "role_permissions",
    Base.metadata,
    Column(
        "role_id", Integer, ForeignKey("roles.id", ondelete="CASCADE"), primary_key=True
    ),
    Column(
        "permission_id",
        Integer,
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    extend_existing=True,  # This allows us to redefine the table if it already exists, which can be useful during development
)
