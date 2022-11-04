from typing import List
from pydantic import BaseModel
from datetime import datetime

from .OptionEnum import OptionEnum


class CopySchema(BaseModel):
    sourcePath: str = "srcPath"
    destinationPath: str = "destPath"

    class Config:
        orm_mode = False


class ListCopySchema(BaseModel):
    type: OptionEnum = OptionEnum.OBJECT
    data: List[CopySchema]

    class Config:
        orm_mode = False
