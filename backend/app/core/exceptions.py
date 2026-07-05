from http import HTTPStatus


class AppException(Exception):
    """Base exception for application errors."""

    def __init__(
        self,
        message: str,
        code: str,
        status_code: HTTPStatus,
    ) -> None:
        self.message = message
        self.code = code
        self.status_code = status_code

        super().__init__(message)


class NotFoundException(AppException):
    """Raised when a requested resource cannot be found."""

    def __init__(
        self,
        code: str,
        message: str,
    ) -> None:
        super().__init__(
            message=message,
            code=code,
            status_code=HTTPStatus.NOT_FOUND,
        )
