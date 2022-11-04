from pydantic import BaseModel
from datetime import datetime


class RolePermissionCreateSchema(BaseModel):
    role_id: int
    permission_id: int

    class Config:
        orm_mode = True
