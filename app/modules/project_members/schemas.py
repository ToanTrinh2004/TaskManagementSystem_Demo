from datetime import datetime
import uuid

from pydantic import BaseModel

from app.modules.project_members.model import ProjectRole


class ProjectMemberInvite(BaseModel):
    project_id : uuid.UUID
    member_id:uuid.UUID  
class ProjectMemberResponse(BaseModel):
    id: uuid.UUID
    project_id: uuid.UUID
    user_id: uuid.UUID
    role: ProjectRole
    created_at: datetime

    model_config = {
        "from_attributes": True
    }