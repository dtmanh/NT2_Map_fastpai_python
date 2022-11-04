from pydantic import BaseModel
from datetime import datetime, time, timedelta

class SourceDataCollectionSchema(BaseModel):
    name: str = None
    description: str = None
    url: str = None
    priority: int = None
    user_id: int = None
    created_at: datetime = datetime.now
    updated_at: datetime = None

    class Config:
        orm_mode = True

class SourceDataCollectionCreateSchema(BaseModel):
    name: str = None
    description: str = None
    url: str = None
    priority: int = None
    user_id: int = None
    is_available: bool = True
    class Config:
        orm_mode = True

class SourceDataCollectionUpdateSchema(BaseModel):
    name: str = None
    description: str = None
    url: str = None
    priority: int = None
    is_available: bool = True
    class Config:
        orm_mode = True
