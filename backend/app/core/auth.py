from bson import ObjectId
from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from jwt import ExpiredSignatureError, InvalidTokenError

from app.core.dependencies import user_repository
from app.core.exceptions import UnauthorizedException
from app.core.security import decode_access_token

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

    user = await user_repository.find_by_id(ObjectId(user_id))

    if user is None:
        raise UnauthorizedException(
            message="Invalid authentication credentials.", code="INVALID_CREDENTIALS"
        )

    return user
