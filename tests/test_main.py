from types import SimpleNamespace


def test_service_is_created():
    from main import main

    assert isinstance(main, SimpleNamespace)
