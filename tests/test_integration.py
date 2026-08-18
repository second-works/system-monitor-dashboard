from fastapi.testclient import TestClient

from app import main


client = TestClient(main.app)


def test_dashboard_assets_and_system_api_are_reachable(monkeypatch) -> None:
    expected = {
        "cpu_percent": 24.1,
        "memory": {"used_gb": 8.5, "total_gb": 16.0, "percent": 53.1},
        "disk": {"used_gb": 143.0, "total_gb": 256.0, "percent": 55.9},
        "os": "macOS",
        "uptime_seconds": 301400,
    }
    monkeypatch.setattr(main, "get_system_info", lambda: expected)

    dashboard = client.get("/", headers={"accept": "text/html"})
    api = client.get("/api/system")
    javascript = client.get("/static/app.js")
    stylesheet = client.get("/static/style.css")

    assert dashboard.status_code == 200
    assert dashboard.headers["content-type"].startswith("text/html")
    assert "System Monitor Dashboard" in dashboard.text
    assert "/static/style.css" in dashboard.text
    assert "/static/app.js" in dashboard.text
    assert javascript.status_code == 200
    assert "updateDashboard" in javascript.text
    assert stylesheet.status_code == 200
    assert ".metrics-grid" in stylesheet.text
    assert api.status_code == 200
    assert api.json() == expected
