from fastapi import FastAPI

app = FastAPI(title="Telemetry Lens API")


@app.get("/")
def root():
    return {"message": "Telemetry Lens backend running"}