import logging
from types import SimpleNamespace

from api_proxy.adapters.web import fastapi
from api_proxy.config import load
from api_proxy.controllers import Controller


def service():
    try:
        config = load()
        logging.basicConfig(
            level=config.logging["level"], format="%(asctime)s [%(levelname)s] %(message)s"
        )
        logger = logging.getLogger(__name__)

        logger.info("Loaded config")

        controller = Controller(logger=logger)
        api_conf = fastapi.WebApiConfig(**config.web_api, version=config.app["version"])
        api = fastapi.create_app(logger=logger, controller=controller, config=api_conf)

        return SimpleNamespace(api=api)
    except Exception as err:
        logger.error(f"Error in service config: {str(err)}")
        return


main = service()
app = main.api
