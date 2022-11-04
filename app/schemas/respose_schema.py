from app.services.mark_map_area.schemas.mark_map_area_schema import MarkMapListSchema
from pydantic import BaseModel

class ListMarkMapResponseSchema(BaseModel):
    status: int = 200
    total_record: int = 0
    message: str = None
    data: list[MarkMapListSchema] = None

    class Config:
        orm_mode = False

class ListResponseSchema(BaseModel):
    status: int = 200
    total_record: int = 0
    message: str = None
    data: object = []

    class Config:
        orm_mode = False


class ListSystemLogsSchema(BaseModel):
    numberOfPages: int
    page_index: int
    page_size: int
    totalRecords: int
    log_list: object = []

    class Config:
        orm_mode = False

class ResultResponseSchema(BaseModel):
    status: int = 200
    message: str = None
    data: object = []

    class Config:
        orm_mode = False

class DetailMarkMapResponseSchema(BaseModel):
    status: int = 200
    message: str = None
    data: MarkMapListSchema = None

    class Config:
        orm_mode = False