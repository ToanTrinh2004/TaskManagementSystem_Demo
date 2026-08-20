from fastapi import FastAPI
app = FastAPI()
from app.middleware.error_handler import register_error_handler
from app.modules.users.router import router as users_router
from app.modules.workspaces.router import router as workspaces_router

app.include_router(users_router, prefix="/api/v1")
app.include_router(workspaces_router, prefix="/api/v1")
register_error_handler(app)

@app.get("/health")
def health_check():
    return {"status": "ok"}