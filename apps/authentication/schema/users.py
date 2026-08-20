from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserRegister(UserBase):
    full_name: str
    password: str


class UserCreate(UserBase):
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    user_type: str = "SYSTEM"


class UserList(UserBase):
    id: int
    user_type: str

    # password: str
    model_config = ConfigDict(from_attributes=True)


class UserRetrieve(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserLogin(BaseModel):
    username: str
    password: str
    # user_type: Optional[str] = None


class LogoutRequest(BaseModel):
    refresh_token: str
