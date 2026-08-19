from fastapi import FastAPI
app = FastAPI()
from app.modules.users.router import router as users_router
app.include_router(users_router, prefix="/api/v1")
@app.get("/health")
def health_check():
    return {"status": "ok"}