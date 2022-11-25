import os

import pytest

INTEGRATION_MARK = "integration"


@pytest.fixture(scope="session")
def monkeypatch_session():
    """Fixture to create manually a session scoped monkeypatch object."""
    from _pytest.monkeypatch import MonkeyPatch

    m = MonkeyPatch()
    yield m
    m.undo()


@pytest.fixture(scope="session", autouse=True)
def configs(monkeypatch_session):
    monkeypatch_session.setenv("ENV", "test")

    from api_proxy import config

    return config.load()


def pytest_addoption(parser):
    """
    Registers new pytest command line options.
        - `--rununit`: when passed, only unit tests are run
    """
    parser.addoption("--rununit", action="store_true", default=False, help="run only unit tests")


def pytest_collection_modifyitems(config, items):
    """This pytest builtin hook contains the list of collected tests,
    so here it'sf used to check if only unit tests should be run,
    and skip all the integration tests."""
    if config.getoption("--rununit"):
        skip_integration = pytest.mark.skip()
        for item in items:
            if INTEGRATION_MARK in item.keywords:
                item.add_marker(skip_integration)
    else:
        os.environ["TEST_INTEGRATION_TESTS_ENABLED"] = "Y"
