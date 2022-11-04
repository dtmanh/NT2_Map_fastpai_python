from pydantic import BaseModel
from datetime import datetime, time, timedelta


class AreaProfileCreateSchema(BaseModel):
    name: str = "name profile area"
    area_id: int = ""
    type: str = "File, Data, Image"
    lever: int = 1
    content: str = ""

    class Config:
        orm_mode = True

class AreaProfileUpdateSchema(BaseModel):
    name: str = "update name profile area"
    area_id: int = 1
    user_id: int = 1
    type: str = "Data"
    lever: int = 1
    content: str = "content data"

    class Config:
        orm_mode = True
