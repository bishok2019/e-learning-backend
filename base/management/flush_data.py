# base/management/flush_data.py
import typer
from sqlalchemy import text
from sqlalchemy.orm import Session

from apps.database import SessionLocal, engine

# Order matters if you're NOT using TRUNCATE ... CASCADE — children before parents.
# With CASCADE (used below) order doesn't matter, but keep this as documentation
# of your FK graph in case you switch strategies later.
TABLES_TO_FLUSH = [
    "api_logs",
    "error_logs",
    # "progress",
    "enrollments",
    "lessons",
    "courses",
    "refresh_tokens",
    "user_roles",
    "user_permissions",
    "role_permissions",
    "roles",
    "permissions",
    "permission_categories",
    "users",
]


def flush_data(
    tables: str = typer.Option(
        None,
        "--tables",
        help="Comma-separated list of specific tables to flush. Defaults to all.",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation prompt."),
):
    """Delete all rows from data tables, keeping schema intact (like Django's flush)."""
    target_tables = (
        [t.strip() for t in tables.split(",")] if tables else TABLES_TO_FLUSH
    )

    if not yes:
        typer.secho(
            f"⚠️  This will DELETE ALL ROWS from: {', '.join(target_tables)}",
            fg=typer.colors.YELLOW,
        )
        confirm = typer.confirm("Are you sure you want to continue?")
        if not confirm:
            typer.echo("Aborted.")
            raise typer.Exit()

    db: Session = SessionLocal()
    try:
        table_list = ", ".join(target_tables)
        db.execute(text(f"TRUNCATE TABLE {table_list} RESTART IDENTITY CASCADE;"))
        db.commit()
        typer.secho(
            f"✅ Flushed {len(target_tables)} table(s): {', '.join(target_tables)}",
            fg=typer.colors.GREEN,
        )
    except Exception as e:
        db.rollback()
        typer.secho(f"❌ Failed to flush data: {e}", fg=typer.colors.RED)
        raise
    finally:
        db.close()
