from fastapi import FastAPI


app = FastAPI(title="System Monitor Dashboard")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok"}
