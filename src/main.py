import logging
from types import SimpleNamespace

from api_proxy.adapters.web import fastapi
from api_proxy.config import load


def service():
    try:
        config = load()
        logging.info("Loaded config")

        api_conf = fastapi.WebApiConfig(**config.web_api, version=config.app["version"])
        api = fastapi.create_app(config=api_conf)

        return SimpleNamespace(api=api)
    except Exception as err:
        logging.error(f"Error in service config: {str(err)}")
        return


main = service()
app = main.api
