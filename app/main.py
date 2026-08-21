import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from redis.asyncio import Redis
from app.core.config import settings
from app.modules.log_activity.activity_consumer import activity_consumer

from app.db.session import get_db
from app.middleware.error_handler import register_error_handler
from app.modules.users.router import router as users_router
from app.modules.workspaces.router import router as workspaces_router
from app.modules.projects.router import router as projects_router
from app.modules.tasks.router import router as tasks_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)
    app.state.redis = redis_client

    db = await anext(get_db())  
    asyncio.create_task(activity_consumer(redis_client, db))

    yield

    await redis_client.close()

app = FastAPI(lifespan=lifespan)
register_error_handler(app)
app.include_router(users_router, prefix="/api/v1")
app.include_router(workspaces_router, prefix="/api/v1")
app.include_router(projects_router, prefix="/api/v1")
app.include_router(tasks_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "ok"}