from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.database import get_db
from base.pagination import get_pagination_params, paginate
from base.route import StandardResponse

from .models import CustomUser
from .schemas import UserCreate, UserList, UserLogin, UserRetrieve, UserUpdate
from .utils import hash_password, verify_password

router = APIRouter()


@router.post(
    "/create", response_model=StandardResponse, status_code=status.HTTP_201_CREATED
)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Create a new user"""
    # Check if user exists already
    existing_user = (
        db.query(CustomUser)
        .filter(
            (CustomUser.username == user.username) | (CustomUser.email == user.email)
        )
        .first()
    )
    if existing_user:
        StandardResponse.error_response(
            message="Username or email already registered.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Create new user
    db_user = CustomUser(
        username=user.username,
        email=user.email,
        hashed_password=hash_password(user.password),
        is_active=True,
        is_superuser=False,
        # is_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return StandardResponse.success_response(
        data=UserRetrieve.model_validate(db_user),
        message="User created successfully.",
    )


@router.get("/list", response_model=StandardResponse)
def get_users(
    # page: int = 1,  # we are passing page and page_size in paginate() directly
    # page_size: int = 1,
    db: Session = Depends(get_db),
    pagination=Depends(get_pagination_params),
):
    """Get all users with pagination"""
    result = paginate(
        query=db.query(CustomUser),
        pagination=pagination,
        schema=UserList,
    )
    return StandardResponse.success_response(
        data=result.data,
        message="Users fetched successfully.",
        meta=result.meta,
    )


@router.get("/retrieve/{user_id}", response_model=StandardResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Get a specific user by ID"""
    user = db.query(CustomUser).filter(CustomUser.id == user_id).first()
    if not user:
        StandardResponse.error_response(
            message="User not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return StandardResponse.success_response(
        data=UserRetrieve.model_validate(user),
        message="User retrieved successfully.",
    )


@router.patch("/update/{user_id}", response_model=StandardResponse)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
):
    """Update a specific user by ID"""
    existing_user = (
        db.query(CustomUser)
        .filter(
            (CustomUser.username == user_update.username)
            | (CustomUser.email == user_update.email)
        )
        .first()
    )
    if existing_user:
        StandardResponse.error_response(
            message="Username or email already registered.",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    user = db.query(CustomUser).filter(CustomUser.id == user_id).first()
    if not user:
        StandardResponse.error_response(
            message="User not found.",
            error="User not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    # Update fields if provided
    if user_update.username is not None:
        user.username = user_update.username
    if user_update.email is not None:
        user.email = user_update.email
    if user_update.password is not None:
        user.hashed_password = hash_password(user_update.password)
    if user_update.is_active is not None:
        user.is_active = user_update.is_active
    if user_update.is_superuser is not None:
        user.is_superuser = user_update.is_superuser

    db.commit()
    db.refresh(user)

    return StandardResponse.success_response(
        data=UserRetrieve.model_validate(user),
        message="User updated successfully.",
    )
