from datetime import datetime
import uuid
from pydantic import BaseModel

from app.modules.log_activity.model import ActivityAction


class ActivityLogResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    project_id: uuid.UUID
    action: ActivityAction
    target_id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True