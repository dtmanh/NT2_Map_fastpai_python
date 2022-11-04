from datetime import date
from fastapi import Query
from pydantic import BaseModel, PositiveInt, validator

from app.services.system_log.schemas.system_log_schema import LOG_ACTION


class HistorySearchCreateSchema(BaseModel):
    data_search: object = {}

    class Config:
        orm_mode = False
