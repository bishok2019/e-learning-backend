from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from apps.authentication.models import RefreshToken, User, UserType
from apps.authentication.schemas import (
    LogoutRequest,
    UserLogin,
    UserRegister,
)
from apps.database import get_db
from base.route import StandardResponse

from .utils import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    hash_password,
    verify_password,
    verify_token,
)

router = APIRouter()


@router.post("/register", response_model=StandardResponse)
def register(user: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    existing_user = (
        db.query(User)
        .filter((User.username == user.username) | (User.email == user.email))
        .first()
    )
    if existing_user:
        StandardResponse.error_response(
            message="Username or email already registered",
            errors=[
                {
                    "field": "username/email",
                    "message": "Username or email already registered",
                }
            ],
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    # Create new user
    try:
        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hash_password(user.password),
            is_active=True,
            is_superuser=False,
            user_type=UserType.CUSTOMER,  # Set user type to CUSTOMER for registered users
            # is_verified=False,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        # if db_user.user_type == UserType.CUSTOMER:
        #     customer_profile = Customer(
        #         user_id=db_user.id,
        #         full_name=user.full_name,
        #         # Add other customer fields here from user or request if needed
        #     )
        #     db.add(customer_profile)
        #     db.commit()

        return StandardResponse.success_response(
            data={
                "id": db_user.id,
                "username": db_user.username,
                "email": db_user.email,
            },
            message="User registered successfully",
        )
    except Exception as e:
        db.rollback()
        StandardResponse.error_response(
            message="An error occurred during registration",
            errors=[{"message": str(e)}],
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.post("/login")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return JWT tokens"""
    # Find user
    user = db.query(User).filter(User.username == user_credentials.username).first()

    if not user or not verify_password(user_credentials.password, user.hashed_password):
        StandardResponse.error_response(
            message="Invalid username or password",
            error="Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    if not user.is_active:
        StandardResponse.error_response(
            message="Inactive user account",
            status_code=status.HTTP_403_FORBIDDEN,
        )

    # Create tokens
    access_token = create_access_token(
        data={
            "sub": str(user.id),
            "user_type": user.user_type.value,
        }
    )
    # refresh_token = create_refresh_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    db_token = RefreshToken(
        user_id=user.id,
        token=refresh_token,
        expires_at=datetime.now() + timedelta(days=7),
    )

    db.add(db_token)
    db.commit()

    return StandardResponse.success_response(
        data={
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                # "user_type": user.user_type.value,
            },
            "roles": [role.name for role in user.user_roles],
            "permissions": [perm.code_name for perm in user.user_permissions],
        },
        message="Login successful",
    )


@router.post("/logout")
def logout(
    schema: LogoutRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    token = (
        db.query(RefreshToken)
        .filter(
            RefreshToken.token == schema.refresh_token,
            RefreshToken.user_id == current_user.id,
        )
        .first()
    )

    if token:
        token.is_blacklisted = True
        db.commit()

    return StandardResponse.success_response(
        data=None,
        message="Logout successful.",
    )


@router.post("/refresh")
def refresh_token(current_refresh_token: str, db: Session = Depends(get_db)):
    """Refresh access token using refresh token"""
    try:
        user_id = verify_token(current_refresh_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        StandardResponse.error_response(
            message="User not found",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    current_refresh_token_record = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == current_refresh_token)
        .first()
    )
    if not current_refresh_token_record:
        StandardResponse.error_response(
            message="Refresh token not found",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    if current_refresh_token_record.is_blacklisted:
        StandardResponse.error_response(
            message="Refresh token is already blacklisted",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    current_refresh_token_record.is_blacklisted = True
    db.commit()

    new_access_token = create_access_token(
        data={"sub": str(user.id), "user_type": user.user_type.value}
    )
    new_refresh_token = create_refresh_token({"sub": str(user.id)})

    db.add(
        RefreshToken(
            token=new_refresh_token,
            user_id=user.id,
            expires_at=datetime.now() + timedelta(days=7),
        )
    )
    db.commit()

    return StandardResponse.success_response(
        data={
            "access_token": new_access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer",
        },
        message="Token refreshed successfully",
    )
