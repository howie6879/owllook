#!/usr/bin/env python
from .config import Config


class DevConfig(Config):
    """
    Dev config for owllook
    """

    # Database config
    REDIS_DICT = dict(
        IS_CACHE=True,
        REDIS_ENDPOINT="localhost",
        REDIS_PORT=6379,
        PASSWORD=None,
        CACHE_DB=0,
        SESSION_DB=1,
        POOLSIZE=10,
    )
    MONGODB = dict(
        HOST="",
        PORT="27017",
        USERNAME='',
        PASSWORD='',
        DATABASE='owllook',
    )
