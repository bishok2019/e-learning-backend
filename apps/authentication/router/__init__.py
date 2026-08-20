from .auth import router as auth_router
from .permissions import router as permission_router
from .roles import router as roles_router
from .user import router as user_router

__all__ = [
    "auth_router",
    "user_router",
    "roles_router",
    "permission_router",
]
