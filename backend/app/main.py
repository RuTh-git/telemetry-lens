from fastapi import FastAPI
from app.routes import session

app = FastAPI(title="Telemetry Lens API")

app.include_router(session.router, prefix="/api/session", tags=["session"])

@app.get("/")
def root():
    return {"message": "Telemetry Lens backend running"}