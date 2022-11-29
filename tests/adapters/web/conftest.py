import pytest
from fastapi.testclient import TestClient

from api_proxy.adapters.web.fastapi import WebApiConfig, create_app
from api_proxy.controllers import Controller


@pytest.fixture(scope="session")
def controller(logger):
    return Controller(logger=logger)


@pytest.fixture(scope="function")
def app(logger, controller):
    config = WebApiConfig(
        title="test app",
        version="test-version",
    )
    return create_app(logger, controller, config)


@pytest.fixture(scope="function")
def client(app):
    return TestClient(app)
