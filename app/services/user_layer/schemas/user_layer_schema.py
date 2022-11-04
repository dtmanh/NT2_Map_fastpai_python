from pydantic import BaseModel
from datetime import datetime, time, timedelta


class UserLayerCreateSchema(BaseModel):
    tags: str = "name tags layer"
    layer_id: str = ""
    geometry: object = {"type": "Polygon",
        "coordinates": []}
    properties: object = {}
    meta_data: object = {}

    class Config:
        orm_mode = True

class UserLayerUpdateSchema(BaseModel):
    tags: str = "name tags layer"
    geometry: object = {"type": "Polygon",
        "coordinates": []}
    properties: object = {}
    meta_data: object = {}

    class Config:
        orm_mode = True

class UserLayerIDSchema(BaseModel):
    layer_id: str = ""

    class Config:
        orm_mode = True
