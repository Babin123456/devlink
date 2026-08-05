from typing import Any, List, Optional, Tuple, TypeVar
from sqlalchemy.orm import Query
from sqlalchemy import desc, asc, inspect

from app.schemas.pagination import PaginatedResponse, encode_cursor, decode_cursor

T = TypeVar("T")


def paginate_query(
    query: Query,
    limit: int = 20,
    cursor: Optional[str] = None,
    offset: Optional[int] = 0,
    sort_column: Optional[Any] = None,
    is_desc: bool = True,
    id_column: Optional[Any] = None,
) -> Tuple[List[Any], int, Optional[str], Optional[str], bool, bool]:
    """
    Paginate a SQLAlchemy query with cursor and offset support.
    Returns (items, total_count, next_cursor, prev_cursor, has_next, has_prev).
    """
    total = query.count()

    cursor_data = decode_cursor(cursor) if cursor else None
    
    # If cursor data contains offset, fallback or use cursor offset
    effective_offset = offset or 0
    if cursor_data and "offset" in cursor_data and not (cursor_data.get("id") or cursor_data.get("val")):
        effective_offset = cursor_data["offset"]

    # Apply cursor filter if sort_column and id_column are available
    if cursor_data and ("val" in cursor_data or "id" in cursor_data):
        c_val = cursor_data.get("val")
        c_id = cursor_data.get("id")
        
        if sort_column is not None and c_val is not None:
            if is_desc:
                query = query.filter(sort_column <= c_val)
            else:
                query = query.filter(sort_column >= c_val)
        elif id_column is not None and c_id is not None:
            if is_desc:
                query = query.filter(id_column <= c_id)
            else:
                query = query.filter(id_column >= c_id)

    # Order query
    if sort_column is not None:
        query = query.order_by(desc(sort_column) if is_desc else asc(sort_column))
    elif id_column is not None:
        query = query.order_by(desc(id_column) if is_desc else asc(id_column))

    # Fetch limit + 1 items to determine has_next
    fetch_limit = limit + 1
    if effective_offset > 0:
        query = query.offset(effective_offset)

    raw_items = query.limit(fetch_limit).all()

    has_next = len(raw_items) > limit
    items = raw_items[:limit]
    has_prev = effective_offset > 0 or (cursor_data is not None)

    next_cursor = None
    prev_cursor = None

    if items:
        last_item = items[-1]
        first_item = items[0]

        # Generate next cursor
        next_data = {}
        if id_column is not None and hasattr(last_item, id_column.key if hasattr(id_column, "key") else "id"):
            next_data["id"] = str(getattr(last_item, id_column.key if hasattr(id_column, "key") else "id"))
        if sort_column is not None and hasattr(last_item, sort_column.key if hasattr(sort_column, "key") else "id"):
            val = getattr(last_item, sort_column.key if hasattr(sort_column, "key") else "id")
            next_data["val"] = str(val) if val is not None else None
        
        if not next_data:
            next_data["offset"] = effective_offset + len(items)

        if has_next:
            next_cursor = encode_cursor(next_data)

        # Generate prev cursor
        if has_prev:
            prev_offset = max(0, effective_offset - limit)
            prev_cursor = encode_cursor({"offset": prev_offset})

    return items, total, next_cursor, prev_cursor, has_next, has_prev


def build_paginated_response(
    items: List[T],
    total: int,
    limit: int,
    next_cursor: Optional[str] = None,
    prev_cursor: Optional[str] = None,
    has_next: bool = False,
    has_prev: bool = False,
) -> PaginatedResponse[T]:
    """Helper to build a PaginatedResponse pydantic model."""
    return PaginatedResponse[T](
        items=items,
        total=total,
        limit=limit,
        next_cursor=next_cursor,
        prev_cursor=prev_cursor,
        has_next=has_next,
        has_prev=has_prev,
    )
