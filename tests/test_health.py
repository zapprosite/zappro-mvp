from fastapi.testclient import TestClient

from src import __version__
from src.config import get_settings
from src.main import app


def test_health_endpoint_returns_status_and_version():
    client = TestClient(app)

    response = client.get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["version"] == __version__
    settings = get_settings()
    assert payload["rate_limit"] == str(settings.rate_limit.max_requests)
    assert payload["rate_limit_window"] == str(settings.rate_limit.window_seconds)
