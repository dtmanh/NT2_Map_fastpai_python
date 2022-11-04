from pydantic import BaseModel
from datetime import datetime


class PermissionCreateSchema(BaseModel):
    permission_name: str = "Your name action"
    key: str = "Key action"
    module: str = "Key module"

    class Config:
        orm_mode = True
