from datetime import datetime
import uuid

from pydantic import Field

from app.db.session import Base


class WorkSpaceCreate(Base):
    name : str = Field( min_length=1, max_length=50)
    description : str = Field( min_length=1, max_length=200)
class WorkSpaceResponse:
    id : uuid.UUID
    name : str
    description : str
    created_at : datetime
    updated_at : datetime

    class Config:
        orm_mode = True