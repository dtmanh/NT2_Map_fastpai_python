from ctypes.wintypes import INT
import json
from typing import List
from pydantic import BaseModel
from datetime import datetime, time, timedelta

class MarkMapListSchema(BaseModel):
    id: int
    name: str="name mark map area"
    description: str=None
    type: str=None
    code: str=None
    geometry: object=None
    properties: object=None
    meta_data: object=None
    active: bool=True
    user_id: int
    user_ids: object=None
    created_at: datetime=None
    updated_at: datetime=None
    class Config:
        orm_mode = True

class MarkMapAreaCreateSchema(BaseModel):
    name: str = "name mark map area"
    geometry: object = {"type": "Polygon",
                        "coordinates": []}
    properties: object = {}
    meta_data: object = {}

    class Config:
        orm_mode = True


class MarkMapAreaUpdateSchema(BaseModel):
    name: str = "name mark map area"
    geometry: object = {"type": "Polygon",
                        "coordinates": []}
    properties: object = {}
    meta_data: object = {}

    class Config:
        orm_mode = True


class MissionProfileCreateSchema(BaseModel):
    name: str = "name mission profile"
    description: str = ""
    user_ids: List[int] = []
    geometry: object = {"type": "Polygon",
        "coordinates": []}
    properties: object = {}
    meta_data: object = {}
    active: bool

    class Config:
        orm_mode = True

class MissionProfileUpdateSchema(BaseModel):
    name: str = "name mission profile"
    description: str = ""
    user_ids: List[int] = []
    geometry: object = {"type": "Polygon",
                        "coordinates": []}
    properties: object = {}
    meta_data: object = {}
    active: bool

    class Config:
        orm_mode = True