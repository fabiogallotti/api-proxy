import logging
from types import SimpleNamespace

from api_proxy.config import load


def service():
    try:
        config = load()
        logging.info("Loaded config")

        return SimpleNamespace(config=config)
    except Exception as err:
        logging.error(f"Error in service config: {str(err)}")
        return


main = service()
