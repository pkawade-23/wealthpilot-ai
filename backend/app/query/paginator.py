import base64
import json
from typing import Any, TypeVar

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import ASCENDING, DESCENDING
from pymongo.asynchronous.collection import AsyncCollection

from app.core.exceptions import BadRequestException
from app.query.models import CursorPage
from app.query.params import QueryParams
from app.query.sorting import SortDirection

T = TypeVar("T")


async def paginate[T](
    *,
    collection: AsyncCollection,
    query: QueryParams,
    model: type[T],
    filter: dict[str, Any] | None = None,
) -> CursorPage[T]:
    """Execute a cursor-based paginated MongoDB query."""

    query_filter = _apply_cursor(
        filter=filter,
        query=query,
    )

    sort = _build_sort(query)

    cursor = collection.find(query_filter).sort(sort).limit(query.limit + 1)

    documents = await cursor.to_list(
        length=query.limit + 1,
    )

    return _build_page(
        documents=documents,
        model=model,
        limit=query.limit,
    )


def _invalid_cursor() -> BadRequestException:
    return BadRequestException(
        message="The supplied cursor is invalid.",
        code="INVALID_CURSOR",
    )


def _encode_cursor(last_id: ObjectId) -> str:
    """Encode the last document ID into an opaque cursor."""
    payload = {
        "last_id": str(last_id),
    }

    json_payload = json.dumps(
        payload,
        separators=(",", ":"),
    )
    encoded = base64.urlsafe_b64encode(json_payload.encode())

    return encoded.decode()


def _decode_cursor(cursor: str) -> ObjectId:
    """Decode an opaque cursor into the last document ID."""
    try:
        decoded = base64.urlsafe_b64decode(cursor.encode()).decode()
        payload = json.loads(decoded)

        return ObjectId(payload["last_id"])

    except (
        InvalidId,
        KeyError,
        TypeError,
        ValueError,
        json.JSONDecodeError,
    ) as err:
        raise _invalid_cursor() from err


def _build_sort(query: QueryParams) -> list[tuple[str, int]]:
    """Build the MongoDB sort specification."""

    direction = DESCENDING if query.sort_direction == SortDirection.DESC else ASCENDING

    return [
        (query.sort_by, direction),
        ("_id", direction),
    ]


def _apply_cursor(
    filter: dict[str, Any] | None,
    query: QueryParams,
) -> dict[str, Any]:
    """Apply cursor filtering to the MongoDB query."""

    query_filter = dict(filter or {})

    if query.cursor is None:
        return query_filter

    last_id = _decode_cursor(query.cursor)

    operator = "$lt" if query.sort_direction == SortDirection.DESC else "$gt"

    query_filter["_id"] = {
        operator: last_id,
    }

    return query_filter


def _map_documents[T](
    documents: list[dict[str, Any]],
    model: type[T],
) -> list[T]:
    """Convert MongoDB documents into Pydantic models."""

    mapped_documents = []

    for document in documents:
        document = document.copy()
        document["id"] = str(document.pop("_id"))
        mapped_documents.append(model.model_validate(document))

    return mapped_documents


def _build_page[T](
    *,
    documents: list[dict[str, Any]],
    model: type[T],
    limit: int,
) -> CursorPage[T]:
    """Build a cursor page from MongoDB documents."""

    has_more = len(documents) > limit

    if has_more:
        documents = documents[:limit]

    items = _map_documents(
        documents=documents,
        model=model,
    )

    next_cursor = None

    if has_more:
        last_document = documents[-1]
        next_cursor = _encode_cursor(last_document["_id"])

    return CursorPage(
        items=items,
        next_cursor=next_cursor,
        has_more=has_more,
        limit=limit,
    )
