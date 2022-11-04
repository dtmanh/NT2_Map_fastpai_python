from pydantic import BaseModel
from datetime import datetime


class CreateFolderSchema(BaseModel):
    folder_path: str = "Your_Folder"

    class Config:
        orm_mode = False
