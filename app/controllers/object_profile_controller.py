import json
from typing import List, Union
import requests
from fastapi import FastAPI
from databases.db import Session, get_db
from fastapi import Depends, APIRouter, Body, Request, Response
from app.services.object_profiles import object_profile_service
from app.services.object_profiles.schemas.object_profile_schema import ObjectProfileUpdateSchema, ObjectProfileCreateSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system import system_service
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
router = APIRouter()
TAG = 'Object Profile'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/object_profile/list/{id}", dependencies=[LOGIN], tags=[TAG])
def get_all_profile(request: Request, id: int, session: Session = DB):
    user_id = system_service.get_current_id(request)
    response = object_profile_service.get_all_by_user_id(session, id, user_id)
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.LIST,
        type=LOG_TYPE.LOG_OBJECT_PROFILE,
        description='Danh sách hồ sơ của khu vực được đánh dấu',
    ))
    return response

@router.post("/object_profile/create", dependencies=[LOGIN], tags=[TAG])
async def area_profile_create(request: Request, session: Session = DB, body: ObjectProfileCreateSchema = Body(...)):
    user_id = system_service.get_current_id(request)
    response = object_profile_service.create_object_profile(session, user_id, body)
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.CREATE,
        type=LOG_TYPE.LOG_OBJECT_PROFILE,
        description='Thêm hồ sơ cho khu vực đánh dấu',
    ))
    if response:
        return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm tài liệu thành công")
    return {"status": 202, "detail": "Không thành công"}

@router.put("/object_profile/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def area_profile_update(request: Request, id: int, session: Session = DB, body: ObjectProfileUpdateSchema = Body(...)):
    user_id = system_service.get_current_id(request)
    response = object_profile_service.update_object_profile(id, session, body)
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.CREATE,
        type=LOG_TYPE.LOG_OBJECT_PROFILE,
        description='Cập nhật hồ sơ khu vực đánh dấu',
    ))
    if response:
        return ListResponseSchema(data=response, total_record=1, status=200, message="Cập nhật thành công")
    return {"status": 202,"detail": "cập nhật không thành công"}

@router.delete("/object_profile/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def area_profile_delete(request: Request, id: int, session: Session = DB):
    user_id = system_service.get_current_id(request)
    response = object_profile_service.delete_object_profile(user_id, id, session)
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.DELETE,
        type=LOG_TYPE.LOG_OBJECT_PROFILE,
        description=f'Xóa khu vực đánh dấu {id}',
    ))

    return response