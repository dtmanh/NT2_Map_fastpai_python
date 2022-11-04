from array import array
import json
from fastapi import Depends, APIRouter, Body, HTTPException, Request, status
from pydantic import PositiveInt
from app.services.auth.auth_bearer import JWTBearer
from databases.db import Session, get_db
from app.services.system_config import system_config_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
from app.services.system_log import system_log_service
from app.services.system import system_service
router = APIRouter()
TAG = 'System Config'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/system-config/list", dependencies=[LOGIN], tags=[TAG])
def get_system_config(request: Request, session: Session = DB):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_SYSTEM_CONFIG,
            description=f'Danh sách cấu hình hệ thống',
            detail = f' xem danh sách cấu hình hệ thống'
        ))

        system_config = system_config_service.get_all(session)
        return system_config
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    


@router.post("/system-config/save", dependencies=[LOGIN], tags=[TAG])
def save_system_config(request: Request, session: Session = DB, body=Body(...)):
    try:
        system_config = system_config_service.save(session, body)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.UPDATE,
            type=LOG_TYPE.LOG_SYSTEM_CONFIG,
            description='Lưu cấu hình hệ thống',
            detail = f'lưu cấu hình hệ thống {body}'
        ))
        return system_config
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    