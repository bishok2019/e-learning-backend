from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import get_pagination_params
from base.route import StandardResponse
from base.utils.query_utils import generic_list_handler

from ..models import CustomPermission
from ..schema import PermissionBaseSchema

router = APIRouter()


@router.get("/list")
def list_permission(
    search: str = "",
    # user_id: int = None,
    is_active: bool = None,
    user_type: str = None,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
    # __: User = Depends(get_current_user),
):
    """List all Customer records with pagination, search, and filters"""
    return generic_list_handler(
        model=CustomPermission,
        schema=PermissionBaseSchema,
        search_fields=[
            "username",
            "email",
        ],
        filter_fields=[
            "user_id",
            "is_active",
            "user_type",
        ],
        db=db,
        pagination=pagination,
        search=search,
        # user_id=user_id,
        is_active=is_active,
        user_type=user_type,
        # eager_loads=[Customer.user],
        # related_mappings={
        #     "email": "user.email",
        # },
    )
