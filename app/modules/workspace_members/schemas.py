import uuid
from datetime import datetime
from pydantic import BaseModel
from enum import Enum as PyEnum
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

class AssignableRole(str, PyEnum):
    ## only allow manager and member roles passed in not allowing pass owner role
    MANAGER = "manager"
    MEMBER = "member"


class MemberRoleUpdate(BaseModel):
    role: AssignableRole