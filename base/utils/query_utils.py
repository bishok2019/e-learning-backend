from typing import Any, Dict, List, Optional, Type

from sqlalchemy import or_
from sqlalchemy.orm import Query, Session, selectinload
from sqlalchemy.sql.sqltypes import String

from base.pagination import paginate
from base.route import StandardResponse

# ---------------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------------


def apply_filters(query: Query, model: Type, filters: Dict[str, Any]) -> Query:
    """Apply exact-match filters to a query, skipping None values."""
    for attr, value in filters.items():
        if value is not None and hasattr(model, attr):
            query = query.filter(getattr(model, attr) == value)
    return query


def apply_search(
    query: Query,
    model: Type,
    search: Optional[str],
    fields: List[str],
) -> Query:
    """
    Apply case-insensitive ILIKE search across the given model fields.

    Only top-level model fields are supported here. For cross-relationship
    searches, filter at the application layer or extend this function with
    explicit joins.
    """
    if not search or not fields:
        return query

    clauses = []
    for field in fields:
        if not hasattr(model, field):
            continue

        column = getattr(model, field)
        columns = getattr(getattr(column, "property", None), "columns", [])
        if not columns or not isinstance(columns[0].type, String):
            continue

        clauses.append(column.ilike(f"%{search}%"))
    if clauses:
        query = query.filter(or_(*clauses))
    return query


def apply_eager_loads(query: Query, relationships: List) -> Query:
    """Wrap each relationship attribute in selectinload and apply to query."""
    if relationships:
        query = query.options(*[selectinload(rel) for rel in relationships])
    return query


# ---------------------------------------------------------------------------
# Result enrichment
# ---------------------------------------------------------------------------


def enrich_with_related(
    items: List[Dict],
    db_items: List[Any],
    mappings: Dict[str, Any],
) -> None:
    """
    Mutate serialised dicts in-place with values from related ORM objects.

    ``mappings`` values can be either a dotted string or a tuple of strings —
    both resolve the same attribute chain on the ORM object:

        {"category_name": "category.name"}   # dotted string (preferred)
        {"category_name": ("category", "name")}  # legacy tuple (still works)
    """
    for item, db_item in zip(items, db_items):
        for key, path in mappings.items():
            parts = path.split(".") if isinstance(path, str) else list(path)
            value = db_item
            for part in parts:
                value = getattr(value, part, None) if value is not None else None
            item[key] = value


# ---------------------------------------------------------------------------
# Generic handler
# ---------------------------------------------------------------------------


def generic_list_handler(
    *,
    model: Type,
    schema: Type,
    search_fields: List[str],
    filter_fields: List[str],
    db: Session,
    pagination,
    search: Optional[str] = "",
    eager_loads: Optional[List] = None,
    related_mappings: Optional[Dict[str, str]] = None,
    **filters: Any,
) -> StandardResponse:
    """
    Generic paginated list handler with search, filtering, and relationship
    enrichment.

    Args:
        model:            SQLAlchemy model class.
        schema:           Pydantic schema used for serialisation.
        search_fields:    Model field names to run ILIKE search against.
        filter_fields:    Model field names to apply exact-match filters on.
        db:               Active SQLAlchemy session.
        pagination:       Pagination params object with ``page`` / ``page_size``.
        search:           Optional search term.
        eager_loads:      Relationship attributes to selectinload.
        related_mappings: Dotted-path mappings added to each serialised item,
                          e.g. ``{"category_name": "category.name"}``.
        **filters:        Keyword arguments matched against ``filter_fields``.
    """
    query = db.query(model)
    query = apply_search(query, model, search, search_fields)
    query = apply_filters(
        query, model, {field: filters.get(field) for field in filter_fields}
    )
    query = apply_eager_loads(query, eager_loads or [])

    result = paginate(query=query, pagination=pagination, schema=schema)

    if related_mappings:
        offset = (pagination.page - 1) * pagination.page_size
        db_items = query.offset(offset).limit(pagination.page_size).all()
        enrich_with_related(result.data, db_items, related_mappings)

    return StandardResponse.success_response(
        data=result.data,
        message=f"{model.__name__} fetched successfully",
        meta=result.meta,
    )
