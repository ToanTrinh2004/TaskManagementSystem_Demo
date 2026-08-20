from datetime import datetime
import uuid

from pydantic import BaseModel, Field



class WorkSpaceCreate(BaseModel):
    name : str = Field( min_length=1, max_length=50)
    description : str = Field( min_length=1, max_length=200)
class WorkSpaceResponse(BaseModel):
    id : uuid.UUID
    name : str
    description : str
    created_at : datetime
    updated_at : datetime

    class Config:
        from_attributes = True

class WorkSpaceUpdate(BaseModel):
    name: str | None = None
    description: str | None = None