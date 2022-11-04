from pydantic import BaseModel
from datetime import datetime

class RobotSourceDataCollectionSchema(BaseModel):
    id: int = None
    name: str = None
    description: str = None
    source_id: int = None
    priority: int = None
    frequency: int = None
    attribute: object = {}
    is_check: bool = False
    start_time: datetime = None
    end_time: datetime = None
    user_id: int = None
    created_at: datetime = None
    updated_at: datetime = None

    class Config:
        orm_mode = True

class RobotSourceDataCollectionCreateSchema(BaseModel):
    name: str = None
    description: str = None
    source_id: int = None
    priority: int = None
    frequency: int = None
    attribute: object = None
    is_check: bool = True
    start_time: datetime = None
    end_time: datetime = None
    user_id: int = None
    created_at: datetime = datetime.now()
    updated_at: datetime = None

    class Config:
        orm_mode = True

class RobotSourceDataCollectionUpdateSchema(BaseModel):
    name: str = None
    description: str = None
    source_id: int = None
    priority: int = None
    frequency: int = None
    attribute: object = None
    is_check: bool = True
    start_time: datetime = None
    end_time: datetime = None
    updated_at: datetime = datetime.now()

    class Config:
        orm_mode = True

class ListRobotSourceDataCollectionSchema(BaseModel):
    status: int = 200
    total_record: int = 0
    message: str = None
    data: list[RobotSourceDataCollectionSchema] = None

    class Config:
        orm_mode = False
