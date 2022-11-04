from pydantic import BaseModel
from datetime import datetime, time, timedelta


class ObjectLayersCreateSchema(BaseModel):
    name: str = "class name"

    class Config:
        orm_mode = True

class ObjectLayersUpdateSchema(BaseModel):
    name: str = "class name"

    class Config:
        orm_mode = True
