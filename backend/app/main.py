from fastapi import FastAPI

app = FastAPI(title="Horse Shelter API")

@app.get("/")
def root():
    return {"message": "Horse Shelter API is running"}

@app.get("/health")
def health():
    return {"status": "ok"}