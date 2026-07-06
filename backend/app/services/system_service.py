from app.core.config import settings


class SystemService:
    """Provides information about the running application."""

    def get_system_info(self) -> dict[str, str]:
        """Return basic system information."""

        return {
            "name": settings.app_name,
            "version": settings.app_version,
            "environment": ("development" if settings.debug else "production"),
        }


system_service = SystemService()
