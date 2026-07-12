from typing import Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")
U = TypeVar("U")


class CursorPage(BaseModel, Generic[T]):
    items: list[T]
    next_cursor: str | None
    has_more: bool


def map_cursor_page(  # noqa: UP047
    page: CursorPage[T],
    model: type[U],
) -> CursorPage[U]:
    return CursorPage(
        items=[model.model_validate(item) for item in page.items],
        next_cursor=page.next_cursor,
        has_more=page.has_more,
    )
