import platform
import time
from typing import TypedDict

import psutil


BYTES_PER_GB = 1024**3


class MemoryInfo(TypedDict):
    used_gb: float
    total_gb: float
    percent: float


class DiskInfo(TypedDict):
    used_gb: float
    total_gb: float
    percent: float


class SystemInfo(TypedDict):
    cpu_percent: float
    memory: MemoryInfo
    disk: DiskInfo
    os: str
    uptime_seconds: int


def _to_gb(value_in_bytes: int) -> float:
    return round(value_in_bytes / BYTES_PER_GB, 1)


def _usage_percent(used: int, total: int) -> float:
    if total <= 0:
        return 0.0
    return round((used / total) * 100, 1)


def _os_name() -> str:
    names = {
        "Darwin": "macOS",
        "Linux": "Linux",
        "Windows": "Windows",
    }
    system_name = platform.system()
    return names.get(system_name, system_name)


def get_system_info() -> SystemInfo:
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    return {
        "cpu_percent": round(psutil.cpu_percent(interval=0.1), 1),
        "memory": {
            "used_gb": _to_gb(memory.used),
            "total_gb": _to_gb(memory.total),
            "percent": round(memory.percent, 1),
        },
        "disk": {
            "used_gb": _to_gb(disk.used),
            "total_gb": _to_gb(disk.total),
            "percent": _usage_percent(disk.used, disk.total),
        },
        "os": _os_name(),
        "uptime_seconds": max(0, int(time.time() - psutil.boot_time())),
    }
