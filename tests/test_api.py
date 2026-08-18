from fastapi.testclient import TestClient

from app import main


client = TestClient(main.app)


def test_system_api_returns_fixed_response_structure(monkeypatch) -> None:
    expected = {
        "cpu_percent": 24.1,
        "memory": {"used_gb": 9.8, "total_gb": 16.0, "percent": 61.2},
        "disk": {"used_gb": 143.0, "total_gb": 256.0, "percent": 55.9},
        "os": "macOS",
        "uptime_seconds": 302400,
    }
    monkeypatch.setattr(main, "get_system_info", lambda: expected)

    response = client.get("/api/system")

    assert response.status_code == 200
    assert response.json() == expected
    assert set(response.json()) == {
        "cpu_percent",
        "memory",
        "disk",
        "os",
        "uptime_seconds",
    }
    assert set(response.json()["memory"]) == {"used_gb", "total_gb", "percent"}
    assert set(response.json()["disk"]) == {"used_gb", "total_gb", "percent"}
