import os

from redis import Redis

DEFAULT_REDIS_HOST = "127.0.0.1"
DEFAULT_REDIS_PORT = "6379"


def create_client() -> Redis:
    host = os.getenv("REDIS_HOST", DEFAULT_REDIS_HOST)
    port = os.getenv("REDIS_PORT", DEFAULT_REDIS_PORT)
    return Redis(host, port=int(port))
