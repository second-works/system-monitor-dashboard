from types import SimpleNamespace

from app import system_info


def test_get_system_info_returns_fixed_structure(monkeypatch) -> None:
    gib = system_info.BYTES_PER_GB
    monkeypatch.setattr(
        system_info.psutil,
        "cpu_percent",
        lambda interval: 24.16,
    )
    monkeypatch.setattr(
        system_info.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(
            used=8 * gib + gib // 2,
            total=16 * gib,
            percent=53.125,
        ),
    )
    monkeypatch.setattr(
        system_info.psutil,
        "disk_usage",
        lambda path: SimpleNamespace(
            used=143 * gib,
            total=256 * gib,
            percent=99.9,
        ),
    )
    monkeypatch.setattr(system_info.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(system_info.psutil, "boot_time", lambda: 1_000.0)
    monkeypatch.setattr(system_info.time, "time", lambda: 302_400.0)

    result = system_info.get_system_info()

    assert result == {
        "cpu_percent": 24.2,
        "memory": {"used_gb": 8.5, "total_gb": 16.0, "percent": 53.1},
        "disk": {"used_gb": 143.0, "total_gb": 256.0, "percent": 55.9},
        "os": "macOS",
        "uptime_seconds": 301400,
    }


def test_get_system_info_returns_valid_real_machine_ranges() -> None:
    result = system_info.get_system_info()

    assert set(result) == {"cpu_percent", "memory", "disk", "os", "uptime_seconds"}
    assert 0 <= result["cpu_percent"] <= 100
    assert result["memory"]["used_gb"] >= 0
    assert result["memory"]["total_gb"] > 0
    assert 0 <= result["memory"]["percent"] <= 100
    assert result["disk"]["used_gb"] >= 0
    assert result["disk"]["total_gb"] > 0
    assert 0 <= result["disk"]["percent"] <= 100
    assert isinstance(result["os"], str) and result["os"]
    assert result["uptime_seconds"] >= 0


def test_disk_percent_matches_used_and_total(monkeypatch) -> None:
    gib = system_info.BYTES_PER_GB
    monkeypatch.setattr(system_info.psutil, "cpu_percent", lambda interval: 0.0)
    monkeypatch.setattr(
        system_info.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(used=gib, total=2 * gib, percent=50.0),
    )
    monkeypatch.setattr(
        system_info.psutil,
        "disk_usage",
        lambda path: SimpleNamespace(
            used=round(11.7 * gib),
            total=round(460.4 * gib),
            percent=99.9,
        ),
    )
    monkeypatch.setattr(system_info.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(system_info.psutil, "boot_time", lambda: 0.0)
    monkeypatch.setattr(system_info.time, "time", lambda: 0.0)

    result = system_info.get_system_info()

    assert result["disk"] == {
        "used_gb": 11.7,
        "total_gb": 460.4,
        "percent": 2.5,
    }


def test_disk_percent_is_zero_when_total_is_zero(monkeypatch) -> None:
    gib = system_info.BYTES_PER_GB
    monkeypatch.setattr(system_info.psutil, "cpu_percent", lambda interval: 0.0)
    monkeypatch.setattr(
        system_info.psutil,
        "virtual_memory",
        lambda: SimpleNamespace(used=gib, total=2 * gib, percent=50.0),
    )
    monkeypatch.setattr(
        system_info.psutil,
        "disk_usage",
        lambda path: SimpleNamespace(used=0, total=0, percent=0.0),
    )
    monkeypatch.setattr(system_info.platform, "system", lambda: "Linux")
    monkeypatch.setattr(system_info.psutil, "boot_time", lambda: 0.0)
    monkeypatch.setattr(system_info.time, "time", lambda: 0.0)

    result = system_info.get_system_info()

    assert result["disk"]["percent"] == 0.0
