from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from app.api.horses import router as horses_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router
from app.api.medical_records import router as medical_records_router
from app.api.procedures import router as procedures_router
from app.api.tasks import router as tasks_router

app = FastAPI(title="Horse Shelter API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:9000",
        "http://127.0.0.1:9000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(horses_router, prefix="/api")
app.include_router(auth_router, prefix="/api")
app.include_router(users_router, prefix="/api")
app.include_router(medical_records_router, prefix="/api")
app.include_router(procedures_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")

app.mount("/media", StaticFiles(directory="media"), name="media")


@app.get("/")
def root():
    return {"message": "Horse Shelter API is running"}


@app.get("/health")
def health():
    return {"status": "ok"}
