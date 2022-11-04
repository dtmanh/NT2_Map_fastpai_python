from typing import List
from pydantic import BaseModel
from datetime import datetime

from .OptionEnum import OptionEnum


class DeleteSchema(BaseModel):
    type: OptionEnum = OptionEnum.OBJECT
    data: List[str]

    class Config:
        orm_mode = False
