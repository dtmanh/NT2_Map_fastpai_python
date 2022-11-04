from pydantic import BaseModel
from datetime import datetime


class RoleCreateSchema(BaseModel):
    role_name: str = "Your role"
    permission: str = "1,2,3"
    is_system: bool = False
    class Config:
        orm_mode = True
