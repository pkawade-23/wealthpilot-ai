from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token
from app.repositories.user_repository import UserRepository

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),  # noqa: B008
):
    try:
        payload = decode_access_token(credentials.credentials)
    except ExpiredSignatureError, InvalidTokenError:
        raise UnauthorizedException(
            message="Invalid authentication credentials.",
            code="INVALID_CREDENTIALS",
        ) from None

    user_id = payload["sub"]

    # user = await user_repository.find_by_id(ObjectId(user_id))
    # user = await auth_service.find_by_id(user_id)
    user = await UserRepository().find_by_id(user_id)  # noqa: B008
    if user is None:
        raise UnauthorizedException(
            message="User Not Found", code="INVALID_CREDENTIALS"
        )

    return user
