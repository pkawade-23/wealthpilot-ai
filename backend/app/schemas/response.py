from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class ErrorResponse(BaseModel):
    code: str
    message: str


class ApiResponse(BaseModel, Generic[T]):
    success: bool
    data: T | None = None
    message: str | None = None
    error: ErrorResponse | None = None

    @classmethod
    def success_response(
        cls,
        data: T | None = None,
        message: str | None = None,
    ) -> ApiResponse[T]:
        return cls(
            success=True,
            data=data,
            message=message,
        )

    @classmethod
    def error_response(
        cls,
        code: str,
        message: str,
    ) -> ApiResponse[T]:
        return cls(
            success=False,
            error=ErrorResponse(
                code=code,
                message=message,
            ),
        )
