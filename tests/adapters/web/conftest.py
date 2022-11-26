import pytest
from fastapi.testclient import TestClient

from api_proxy.adapters.web.fastapi import WebApiConfig, create_app


@pytest.fixture(scope="function")
def app():
    config = WebApiConfig(
        title="test app",
        version="test-version",
    )
    return create_app(config)


@pytest.fixture(scope="function")
def client(app):
    return TestClient(app)
