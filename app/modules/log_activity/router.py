import uuid
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.dependencies import get_current_user
from app.db.session import get_db
from app.modules.log_activity.service import ActivityLogService

router = APIRouter(prefix="/projects/{project_id}/logs", tags=["Activity Logs"])


