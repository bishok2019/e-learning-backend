# manage.py
import typer

from apps import model_registry
from base.management import create_superuser, flush_data, seed_permissions

app = typer.Typer(help="Management commands")


@app.callback()
def callback():
    """E-Learning backend management CLI."""
    pass


app.command(name="seed_permissions")(seed_permissions)
app.command(name="flush_data")(flush_data)
app.command(name="createsuperuser")(create_superuser)

if __name__ == "__main__":
    app()
