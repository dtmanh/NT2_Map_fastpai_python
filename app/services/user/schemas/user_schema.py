from pydantic import BaseModel
from datetime import datetime, time, timedelta


class UserSchema(BaseModel):
    id: int
    email: str
    role_id: int

    class Config:
        orm_mode = True
