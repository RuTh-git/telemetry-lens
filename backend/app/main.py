from fastapi import FastAPI
from app.routes import session, telemetry

app = FastAPI(title="Telemetry Lens API")

app.include_router(session.router, prefix="/api/session", tags=["session"])
app.include_router(telemetry.router, prefix="/api/telemetry", tags=["telemetry"])


@app.get("/")
def root():
    return {"message": "Telemetry Lens backend running"}