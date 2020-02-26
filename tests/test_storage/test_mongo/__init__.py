import os

from pymongo import MongoClient

DEFAULT_MONGO_HOST = "127.0.0.1"
DEFAULT_MONGO_PORT = 27017


def create_client() -> MongoClient:
    host = os.getenv("MONGO_HOST", DEFAULT_MONGO_HOST)
    port = os.getenv("MONGO_PORT", DEFAULT_MONGO_PORT)
    return MongoClient(host, port)
