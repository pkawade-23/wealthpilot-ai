from pydantic import BaseModel, Field

from app.query.sorting import SortDirection


class QueryParams(BaseModel):
    cursor: str | None = None

    limit: int = Field(
        default=20,
        ge=1,
        le=100,
    )

    sort_by: str = "created_at"

    sort_direction: SortDirection = SortDirection.DESC

    search: str | None = None
