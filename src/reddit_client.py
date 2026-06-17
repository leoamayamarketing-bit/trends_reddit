import praw
from src.config import RedditConfig


def create_client(config: RedditConfig):
    if config.is_readonly():
        return praw.Reddit(
            client_id=config.client_id,
            client_secret=config.client_secret,
            user_agent=config.user_agent,
        )
    return praw.Reddit(
        client_id=config.client_id,
        client_secret=config.client_secret,
        user_agent=config.user_agent,
        username=config.username,
        password=config.password,
    )


def hot_posts(subreddit: str, limit: int = 10):
    cfg = RedditConfig()
    reddit = create_client(cfg)
    sub = reddit.subreddit(subreddit)
    return [(p.title, p.score, p.url, p.id) for p in sub.hot(limit=limit)]


def new_posts(subreddit: str, limit: int = 10):
    cfg = RedditConfig()
    reddit = create_client(cfg)
    sub = reddit.subreddit(subreddit)
    return [(p.title, p.score, p.url, p.id) for p in sub.new(limit=limit)]


def top_posts(subreddit: str, limit: int = 10, time_filter: str = "day"):
    cfg = RedditConfig()
    reddit = create_client(cfg)
    sub = reddit.subreddit(subreddit)
    return [(p.title, p.score, p.url, p.id) for p in sub.top(limit=limit, time_filter=time_filter)]


def post_details(post_id: str):
    cfg = RedditConfig()
    reddit = create_client(cfg)
    submission = reddit.submission(id=post_id)
    submission.comments.replace_more(limit=0)
    comments = [
        (c.author.name if c.author else "[deleted]", c.body[:200])
        for c in submission.comments.list()[:10]
    ]
    return {
        "title": submission.title,
        "author": submission.author.name if submission.author else "[deleted]",
        "score": submission.score,
        "url": submission.url,
        "selftext": submission.selftext[:500] if submission.selftext else "(no text)",
        "comments": comments,
    }


def search(query: str, subreddit: str | None = None, limit: int = 10):
    cfg = RedditConfig()
    reddit = create_client(cfg)
    if subreddit:
        results = reddit.subreddit(subreddit).search(query, limit=limit)
    else:
        results = reddit.subreddit("all").search(query, limit=limit)
    return [(p.title, p.score, p.url, p.subreddit.display_name, p.id) for p in results]
