from pydantic import BaseModel
from datetime import datetime, time, timedelta


class ObjectCreateSchema(BaseModel):
    name: str = "name điểm"
    description: str = "Mô tả"
    tags: str = "Tag1, tag2"
    image: object = {}
    object_layer_id: int
    properties: object = {}
    geometry: object = {"type": "Polygon",
        "coordinates": []}

    class Config:
        orm_mode = True

class ObjectUpdateSchema(BaseModel):
    name: str = "name điểm"
    description: str = "Mô tả"
    tags: str = "Tag1, tag2"
    image: object = {}
    object_layer_id: int
    properties: object = {}
    geometry: object = {"type": "Polygon",
        "coordinates": []}

    class Config:
        orm_mode = True

class ObjectIDSchema(BaseModel):
    page_size: int = 10
    page_index: int = 0
    filter: object = {}
    object_layer_id: int = 0

    class Config:
        orm_mode = True


