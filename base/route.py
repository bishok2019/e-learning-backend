from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field


class StandardResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    status_code: Optional[int] = Field(default=None)
    error: Optional[str] = None
    errors: Optional[List[Dict[str, str]]] = None
    meta: Dict[str, Any] = Field(
        default_factory=lambda: {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    )

    @classmethod
    def success_response(
        cls,
        data: Any = None,
        message: str = "Operation successful",
        status_code: int = status.HTTP_200_OK,
        meta: Optional[Dict[str, Any]] = None,
    ) -> "StandardResponse":
        base_meta = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        return cls(
            success=True,
            data=data,
            status_code=status_code,
            message=message,
            meta={**base_meta, **(meta or {})},
        )

    @classmethod
    def error_response(
        cls,
        message: str = "Error occurred",
        error: Optional[str] = None,
        errors: Optional[List[Dict[str, str]]] = None,
        meta: Optional[Dict[str, Any]] = None,
        status_code: int = status.HTTP_400_BAD_REQUEST,
    ):
        base_meta = {"timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        raise HTTPException(
            status_code=status_code,
            detail=cls(
                success=False,
                message=message,
                error=error,
                errors=errors,
                meta={**base_meta, **(meta or {})},
                status_code=status_code,
            ).model_dump(),
        )
