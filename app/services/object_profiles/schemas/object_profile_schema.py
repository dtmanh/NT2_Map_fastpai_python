from pydantic import BaseModel
from datetime import datetime, time, timedelta


class ObjectProfileCreateSchema(BaseModel):
    name: str = "name object profile "
    description: str = ""
    content: str = ""
    geometry: object = {}
    properties: object = {}
    type: str = "File, Data, Image"

    class Config:
        orm_mode = True

class ObjectProfileUpdateSchema(BaseModel):
    name: str = "name object profile"
    description: str = ""
    content: str = ""
    geometry: object = {}
    properties: object = {}
    type: str = "File, Data, Image"

    class Config:
        orm_mode = True
