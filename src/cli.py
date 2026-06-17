import click
from src.reddit_client import hot_posts, new_posts, top_posts, post_details, search
from src.trends_client import interest_over_time, related_queries
from src.setup import run_setup, show_status


@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """mi-script-cli - Reddit CLI tool
    
    \b
    Antes de usar, configura tu API key:
      python -m src.cli setup
    """
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


@cli.command()
def setup():
    """Guía interactiva para crear y guardar tu Reddit API key"""
    run_setup()


@cli.command()
def status():
    """Verifica si las credenciales de Reddit están configuradas"""
    show_status()


@cli.command()
@click.argument("subreddit")
@click.option("--limit", default=10, help="Number of posts")
def hot(subreddit, limit):
    """Hot posts from a subreddit"""
    for title, score, url, _ in hot_posts(subreddit, limit):
        click.echo(f"[{score:4d}] {title}")
        click.echo(f"       {url}")
        click.echo()


@cli.command()
@click.argument("subreddit")
@click.option("--limit", default=10, help="Number of posts")
def new(subreddit, limit):
    """New posts from a subreddit"""
    for title, score, url, _ in new_posts(subreddit, limit):
        click.echo(f"[{score:4d}] {title}")
        click.echo(f"       {url}")
        click.echo()


@cli.command()
@click.argument("subreddit")
@click.option("--limit", default=10, help="Number of posts")
@click.option("--time", "time_filter", default="day", help="Time filter: hour, day, week, month, year, all")
def top(subreddit, limit, time_filter):
    """Top posts from a subreddit"""
    for title, score, url, _ in top_posts(subreddit, limit, time_filter):
        click.echo(f"[{score:4d}] {title}")
        click.echo(f"       {url}")
        click.echo()


@cli.command()
@click.argument("post_id")
def details(post_id):
    """Show post details and comments"""
    info = post_details(post_id)
    click.echo(f"Title: {info['title']}")
    click.echo(f"Author: {info['author']} | Score: {info['score']}")
    click.echo(f"URL: {info['url']}")
    click.echo(f"\n{info['selftext']}")
    click.echo("\n--- Comments ---")
    for author, body in info["comments"]:
        click.echo(f"\n{author}: {body}")


@cli.command()
@click.argument("query")
@click.option("--subreddit", "-s", help="Subreddit to search in")
@click.option("--limit", default=10, help="Number of results")
def search_cmd(query, subreddit, limit):
    """Search Reddit"""
    for title, score, url, sub, _ in search(query, subreddit, limit):
        click.echo(f"[{score:4d}] r/{sub} - {title}")
        click.echo(f"       {url}")
        click.echo()


@cli.command()
@click.argument("keyword")
@click.option("--timeframe", default="now 7-d", help="Periodo: now 1-d, now 7-d, today 1-m, today 3-m, today 12-m, today 5-y")
@click.option("--geo", default="", help="Código de país (ej: US, MX, ES)")
def trends(keyword, timeframe, geo):
    """Google Trends: interés en el tiempo"""
    click.echo(interest_over_time(keyword, timeframe, geo))


@cli.command()
@click.argument("keyword")
@click.option("--geo", default="", help="Código de país (ej: US, MX, ES)")
def related(keyword, geo):
    """Google Trends: consultas relacionadas"""
    click.echo(related_queries(keyword, geo))


if __name__ == "__main__":
    cli()
