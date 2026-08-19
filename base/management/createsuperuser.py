import re

import typer
from sqlalchemy.orm import Session

from apps.authentication.models.users import CustomUser, UserType
from apps.authentication.utils import hash_password
from apps.database import SessionLocal

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def create_superuser(
    username: str = typer.Option(..., prompt=True),
    email: str = typer.Option(..., prompt=True),
    password: str = typer.Option(
        ..., prompt=True, hide_input=True, confirmation_prompt=True
    ),
):
    """Create a superuser account."""
    if not EMAIL_REGEX.match(email):
        typer.secho("❌ Invalid email format.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    if len(password) < 8:
        typer.secho("❌ Password must be at least 8 characters.", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    db: Session = SessionLocal()
    try:
        existing = (
            db.query(CustomUser)
            .filter((CustomUser.username == username) | (CustomUser.email == email))
            .first()
        )
        if existing:
            field = "username" if existing.username == username else "email"
            typer.secho(
                f"❌ A user with that {field} already exists.", fg=typer.colors.RED
            )
            raise typer.Exit(code=1)

        user = CustomUser(
            username=username,
            email=email,
            hashed_password=hash_password(password),
            is_active=True,
            is_superuser=True,
            user_type=UserType.SYSTEM,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        typer.secho(
            f"✅ Superuser '{username}' ({email}) created with id={user.id}.",
            fg=typer.colors.GREEN,
        )
    except Exception as e:
        db.rollback()
        typer.secho(f"❌ Failed to create superuser: {e}", fg=typer.colors.RED)
        raise
    finally:
        db.close()
