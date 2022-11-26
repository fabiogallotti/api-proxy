from fastapi.testclient import TestClient


def test_app_healthcheck(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"version": "test-version"}


def test_app_autogenerated_openapi_spec(client):
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert {"openapi", "info", "paths"}.issubset(response.json().keys())


def test_should_return_404_for_unknown_routes(client):
    response = client.get("/not-existent-route")
    assert response.status_code == 404


def test_unhandled_error_exception_handler(app):
    def breaking_function():
        raise KeyError("error")

    app.add_api_route("/broken", breaking_function, methods=["GET"])
    client = TestClient(app, raise_server_exceptions=False)

    response = client.get("/broken")
    assert response.status_code == 500