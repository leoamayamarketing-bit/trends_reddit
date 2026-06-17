import os
from dotenv import load_dotenv

load_dotenv()


class RedditConfig:
    def __init__(self):
        self.client_id = os.getenv("REDDIT_CLIENT_ID")
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET")
        self.user_agent = os.getenv("REDDIT_USER_AGENT")
        self.username = os.getenv("REDDIT_USERNAME")
        self.password = os.getenv("REDDIT_PASSWORD")

    def is_valid(self) -> bool:
        return all([self.client_id, self.client_secret, self.user_agent])

    def is_readonly(self) -> bool:
        return self.is_valid() and not (self.username and self.password)
