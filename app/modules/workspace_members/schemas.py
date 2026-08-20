import uuid
from datetime import datetime
from pydantic import BaseModel
from app.modules.workspace_members.model import WorkSpaceRole


class MemberInvite(BaseModel):
    user_id : uuid.UUID

class MemberResponse(BaseModel):
    id : uuid.UUID
    workspace_id : uuid.UUID
    user_id : uuid.UUID
    role : WorkSpaceRole
    created_at : datetime

    class Config:
        from_attributes = True