from fastapi import FastAPI

from app.system_info import SystemInfo, get_system_info


app = FastAPI(title="System Monitor Dashboard")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/system")
def read_system_info() -> SystemInfo:
    return get_system_info()
