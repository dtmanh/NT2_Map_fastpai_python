from pydantic import BaseModel
from datetime import datetime, time, timedelta


class ObjectEquipmentCreateSchema(BaseModel):
    description: str = "Mô tả ..."
    radius: float = 100
    quantity: int = 1
    attributes: object = {"radius": "200",
      "weight": 1,
      "color": "#d32f2f",
        }
    equipment_id: int= 0
    object_id: int= 0
    class Config:
        orm_mode = True

class ObjectEquipmentUpdateSchema(BaseModel):
    description: str = "Mô tả ..."
    radius: float = 100
    quantity: int = 1
    attributes: object = {"radius": "200",
      "weight": 1,
      "color": "#d32f2f",
        }

    class Config:
        orm_mode = True

class ObjectEquipmentIDSchema(BaseModel):
    page_size: int = 10
    page_index: int = 0
    filter: object = {}

    class Config:
        orm_mode = True

