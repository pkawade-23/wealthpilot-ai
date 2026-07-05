from fastapi import APIRouter

from app.core.config import settings
from app.schemas.response import ApiResponse

router = APIRouter(tags=["Health"])


@router.get("/")
async def root():
    return {
        "message": f"Welcome to {settings.app_name}",
        "version": settings.app_version,
    }


@router.get("/health")
async def health():
    return ApiResponse.success_response({"status": "healthy"})
