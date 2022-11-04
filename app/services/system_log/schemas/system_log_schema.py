
from enum import Enum
from pydantic import BaseModel
from datetime import datetime


class LOG_TYPE(str, Enum):
    LOG_MANAGER = 'System Log Active'
    LOG_CATEGORY = 'System Log Category'
    LOG_PERMISSION = 'System Log Role Permission'
    LOG_MARK_AREA = 'System Log Mark Area'
    LOG_OBJECT_PROFILE = 'System Log Object Profile'
    LOG_USER_LAYER = 'System Log User Layer'
    LOG_OBJECT = 'System Log Object'
    LOG_MISSION_PROFILE = 'System Log Mission Profile'
    LOG_EQUIPMENT = 'System Log Equipment'
    LOG_OBJECT_EQUIPMENT = 'System Log Object Equipment'
    LOG_SYSTEM_CONFIG = 'System Log config'
    LOG_SATELLITE_SEARCH = 'System Log satellite search'
    LOG_SOUCE_DATA_COLLECTION = 'System Log souce data collection'


class LOG_ACTION(str, Enum):
    LOGIN = "Login"
    LOGOUT = "Logout"
    VIEW = "View"
    CREATE = "Create"
    EDIT = "Edit"
    UPDATE = "Update"
    DELETE = "Delete"
    EXPORT = "Export"
    DETAIL = "Detail"
    SEARCH = "SEARCH"
    LIST = "LIST"
    MOVE = "MOVE"
    ADD_SEARCH_HISTORY = "Add_Search_History"
    SEARCH_HISTORY = "History_search_view"
    UPDATE_FILLTER_SEARCH = "Update_Fillter_Search"
    GET_FILLTER_SEARCH = "Get_Fillter_Search"
    RESET_PASSWORD = "Reset_Pasword"

class SystemLogCreateSchema(BaseModel):
    user_id: int
    action: str
    type: str
    method: str
    url: str
    ip: str
    user_agent: str
    accept: str
    desciption: str
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True


class OverideSystemLogSchema(BaseModel):
    type: str = None
    action: str = None
    description: str = None
    detail: str = None
    access_token: str = None
    warehouse: str = None

    class Config:
        orm_mode = True

class MAP_TYPE(str, Enum):
    POINT = "point"
    POLYGON = "polygon"
    MISSION = "mission"
    AREA = "area"