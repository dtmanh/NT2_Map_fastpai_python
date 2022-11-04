from pydantic import BaseModel
from datetime import datetime

from .OptionEnum import OptionEnum


class GetListChildrenSchema(BaseModel):
    selectedPath: str = None
    page_index: int = None
    page_size: int = None
    type: OptionEnum = OptionEnum.FOLDER

    class Config:
        orm_mode = False
