from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class PermissionBaseSchema(BaseModel):
    name: str
    code_name: str
    model_config = ConfigDict(from_attributes=True)


class RoleBaseSchema(BaseModel):
    name: str
    description: str
    is_actiive: bool


class RoleRetrieveSchema(RoleBaseSchema):
    permissions: list[PermissionBaseSchema] = Field(default_factory=list)
