import logging

import pytest


@pytest.fixture(scope="session")
def logger():
    logging.basicConfig(level="INFO", format="%(asctime)s [%(levelname)s] %(message)s")
    return logging.getLogger(__name__)
