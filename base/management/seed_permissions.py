import typer
from sqlalchemy.orm import Session

from apps.authentication.models.roles_permissions import (
    CustomPermission,
    PermissionCategory,
)
from apps.authentication.permission_list import ALL_PERMISSION_LIST
from apps.database import SessionLocal


def _get_or_create_category(
    db: Session, name: str, cache: dict[str, PermissionCategory]
) -> PermissionCategory:
    if name in cache:
        return cache[name]

    category = (
        db.query(PermissionCategory).filter(PermissionCategory.name == name).first()
    )
    if not category:
        category = PermissionCategory(name=name)
        db.add(category)
        db.flush()

    cache[name] = category
    return category


def seed_permissions():
    """Seed permission categories and permissions from ALL_PERMISSION_LIST (idempotent)."""
    db = SessionLocal()
    created, skipped = 0, 0

    try:
        existing_codenames = {
            row[0] for row in db.query(CustomPermission.code_name).all()
        }
        existing_names = {row[0] for row in db.query(CustomPermission.name).all()}
        category_cache: dict[str, PermissionCategory] = {}
        seen_this_run: set[str] = set()  # guards against dupes within the dict itself

        for app_label, models in ALL_PERMISSION_LIST.items():
            category = _get_or_create_category(db, app_label, category_cache)

            for model_name, actions in models.items():
                for action in actions:
                    code_name = f"can_{action}_{model_name}"
                    display_name = (
                        f"{action.capitalize()} {model_name.replace('_', ' ')}"
                    )

                    if (
                        code_name in existing_codenames
                        or display_name in existing_names
                        or code_name in seen_this_run
                    ):
                        skipped += 1
                        continue

                    db.add(
                        CustomPermission(
                            name=display_name,
                            code_name=code_name,
                            category_id=category.id,
                        )
                    )
                    seen_this_run.add(code_name)
                    created += 1

        db.commit()
        typer.secho(
            f"✅ Permissions seeded: {created} created, {skipped} already existed.",
            fg=typer.colors.GREEN,
        )
    except Exception as e:
        db.rollback()
        typer.secho(f"❌ Failed to seed permissions: {e}", fg=typer.colors.RED)
        raise
    finally:
        db.close()
