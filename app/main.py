from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.system_info import SystemInfo, get_system_info


app = FastAPI(title="System Monitor Dashboard")
APP_DIR = Path(__file__).resolve().parent

app.mount("/static", StaticFiles(directory=APP_DIR / "static"), name="static")


@app.get("/", response_model=None)
def read_root(request: Request) -> FileResponse | dict[str, str]:
    if "text/html" in request.headers.get("accept", ""):
        return FileResponse(APP_DIR / "templates" / "index.html", media_type="text/html")
    return {"status": "ok"}


@app.get("/api/system")
def read_system_info() -> SystemInfo:
    return get_system_info()
