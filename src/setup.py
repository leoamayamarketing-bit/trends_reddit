import os
import webbrowser
import click
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
ENV_TEMPLATE = """# Reddit API Credentials
# Creados por mi-script-cli setup
REDDIT_CLIENT_ID={client_id}
REDDIT_CLIENT_SECRET={client_secret}
REDDIT_USER_AGENT=mi-script-cli/1.0 (by /u/{username})
REDDIT_USERNAME={username}
REDDIT_PASSWORD={password}
"""

REDIRECT_URI = "http://localhost:8080"


def run_setup():
    click.clear()
    click.echo("=" * 60)
    click.echo("  Configuración de Reddit API Key para mi-script-cli")
    click.echo("=" * 60)

    click.echo()
    click.echo("Paso 1: Abrir Reddit App Preferences en tu navegador...")
    click.echo()
    click.echo("  Ve a esta URL:")
    click.echo(f"  https://www.reddit.com/prefs/apps")
    click.echo()
    if click.confirm("  Abrir el navegador ahora?", default=True):
        webbrowser.open("https://www.reddit.com/prefs/apps")

    click.echo()
    click.echo("  Una vez allí:")
    click.echo(f"  1. Haz clic en 'Create App' o 'Create Another App'")
    click.echo(f"  2. Name: mi-script-cli")
    click.echo(f"  3. App type: script")
    click.echo(f"  4. Redirect uri: {REDIRECT_URI}")
    click.echo(f"  5. Haz clic en 'Create app'")
    click.echo()
    click.pause("  Presiona Enter cuando hayas creado la app...")

    click.echo()
    click.echo("Paso 2: Ingresa las credenciales")
    click.echo("  (El client_id está debajo del nombre de la app, client_seast es el secreto)")
    click.echo()

    client_id = click.prompt("  Client ID", type=str)
    client_secret = click.prompt("  Client Secret", type=str)
    username = click.prompt("  Tu usuario de Reddit", type=str)
    password = click.prompt("  Tu contraseña de Reddit", type=str, hide_input=True)

    content = ENV_TEMPLATE.format(
        client_id=client_id,
        client_secret=client_secret,
        username=username,
        password=password,
    )

    ENV_PATH.write_text(content)
    os.chmod(ENV_PATH, 0o600)

    click.echo()
    click.echo("=" * 60)
    click.echo("  ✅ Credenciales guardadas en .env")
    click.echo()
    click.echo("  Ahora puedes usar los comandos:")
    click.echo("    python -m src.cli hot python")
    click.echo("    python -m src.cli new python --limit 5")
    click.echo("    python -m src.cli top python --time week")
    click.echo("    python -m src.cli search 'raspberry pi'")
    click.echo("=" * 60)


def show_status():
    if not ENV_PATH.exists():
        click.echo("❌ No hay .env configurado. Ejecuta:")
        click.echo("   python -m src.cli setup")
        return

    from src.config import RedditConfig

    cfg = RedditConfig()
    if cfg.is_valid():
        masked_id = cfg.client_id[:6] + "..." if cfg.client_id else "N/A"
        click.echo(f"✅ Reddit API configurada")
        click.echo(f"   Client ID: {masked_id}")
        click.echo(f"   User:      {cfg.username or '(solo lectura)'}")
    else:
        click.echo("⚠️  .env existe pero faltan campos requeridos (client_id, client_secret, user_agent)")
