from fastapi import FastAPI

from app.api.horses import router as horses_router

app = FastAPI(title="Horse Shelter API")

app.include_router(horses_router, prefix="/api")


@app.get("/")
def root():
    return {"message": "Horse Shelter API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}