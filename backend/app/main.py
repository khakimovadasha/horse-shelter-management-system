from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.horses import router as horses_router

app = FastAPI(title="Horse Shelter API")

app.include_router(horses_router, prefix="/api")
app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
def root():
    return {"message": "Horse Shelter API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}