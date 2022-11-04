from pydantic import BaseModel
from datetime import datetime, time, timedelta


class EquipmentCreateSchema(BaseModel):
    name: str = "Tên thiết bị"
    code: str = "MTB01"
    radius: float = 200
    description: str = "Mô tả ..."
    attributes: object = {"radius": "200",
      "weight": 1,
      "color": "#d32f2f",
        }

    class Config:
        orm_mode = True

class EquipmentUpdateSchema(BaseModel):
    name: str = "Tên thiết bị"
    code: str = "MTB01"
    radius: float = 200
    description: str = "Mô tả ..."
    attributes: object = {"radius": "200",
      "weight": 1,
      "color": "#d32f2f",
        }

    class Config:
        orm_mode = True

class EquipmentIDSchema(BaseModel):
    page_size: int = 10
    page_index: int = 0
    filter: object = {}

    class Config:
        orm_mode = True


