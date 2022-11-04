from pydantic import BaseModel
from datetime import datetime, time, timedelta


class UserClassCreateSchema(BaseModel):
    name: str = "class name"
    layer_id: str = ""
    data: object = {}

    class Config:
        orm_mode = True

class UserClassUpdateSchema(BaseModel):
    name: str = "class name"
    data: object = {}

    class Config:
        orm_mode = True

class UserClassIDSchema(BaseModel):
    layer_id: str = ""

    class Config:
        orm_mode = True
