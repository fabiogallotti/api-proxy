import os
from types import SimpleNamespace


def load():
    return SimpleNamespace(
        app={
            "name": "api_proxy",
            "env": os.getenv("ENV", "test"),
            "version": os.getenv("VERSION", "v1"),
        },
        logging={
            "level": os.getenv("LOG_LEVEL", "DEBUG"),
        },
        web_api={
            "title": os.getenv("WEBAPP_TITLE", "Api Proxy"),
            "root_path": os.getenv("WEBAPP_ROOT_PATH", None),
        },
    )
