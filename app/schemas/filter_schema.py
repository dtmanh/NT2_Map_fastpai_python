from pydantic import BaseModel
class FilterSchema(BaseModel):
    page_size: int = 10
    page_index: int = 0
    filter: object = {}
    class Config:
        orm_mode = False
