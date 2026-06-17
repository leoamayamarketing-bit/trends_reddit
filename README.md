# trends_reddit

CLI para consultar Reddit y Google Trends desde terminal.

## Requisitos

- Python 3.14+
- Homebrew

## Instalación

```bash
cd mi-script-cli
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Configuración (Reddit)

```bash
python -m src.cli setup
```

## Uso

```bash
# Sin argumentos — menú interactivo
./demo.sh

# Con palabra clave directo
./demo.sh Lego

# Google Trends
python -m src.cli trends Lego

# Reddit
python -m src.cli hot lego --limit 10
python -m src.cli search "lego technic"
```

## Comandos disponibles

| Comando | Descripción |
|---------|-------------|
| `trends <keyword>` | Google Trends: interés en el tiempo |
| `related <keyword>` | Google Trends: consultas relacionadas |
| `hot <subreddit>` | Posts populares de un subreddit |
| `top <subreddit>` | Top posts por período |
| `search <query>` | Buscar en Reddit |
| `details <post_id>` | Detalle y comentarios de un post |
| `setup` | Configurar credenciales de Reddit |
| `status` | Verificar configuración |
