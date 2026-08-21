import uuid

from pydantic import BaseModel, Field


class ProjectCreate(BaseModel):
    name : str = Field(min_length=1, max_length=50)
    description : str | None = Field(default=None, max_length=200)
    workspace_id : uuid.UUID

class ProjectResponse(BaseModel):
    id : uuid.UUID
    name : str
    description : str | None
    workspace_id : uuid.UUID
    created_by : uuid.UUID

    class Config:
        from_attributes = True