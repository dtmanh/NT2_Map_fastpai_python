import json
from typing import List, Union
import requests
from fastapi import FastAPI
from databases.db import Session, get_db
from fastapi import Depends, APIRouter, Body, Request, Response
from app.services.user_class import user_class_service
from app.services.user_class.schemas.user_class_schema import UserClassUpdateSchema, UserClassIDSchema, UserClassCreateSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system import system_service
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
router = APIRouter()
TAG = 'User Class'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/user_class/list", dependencies=[LOGIN], tags=[TAG])
async def get_all_class(request: Request, session: Session = DB):
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.LIST,
        type=LOG_TYPE.LOG_USER_CLASS,
        description='Danh sách lớp của người dùng',
    ))

    user_id = system_service.get_current_id(request)
    response = user_class_service.get_all_by_user_id(session, user_id)

    return response

@router.post("/user_class/create", dependencies=[LOGIN], tags=[TAG])
async def user_class_create(request: Request, session: Session = DB, body: UserClassCreateSchema = Body(...)):
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.CREATE,
        type=LOG_TYPE.LOG_USER_CLASS,
        description='Thêm lớp cho người dùng',
    ))
    user_id = system_service.get_current_id(request)

    response = user_class_service.create_user_class(session, user_id, body)
    if response:
        return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm lớp thành công")
    return {"status": 202, "detail": "Không thành công"}

@router.put("/user_class/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def user_class_update(request: Request, id: int, session: Session = DB, body: UserClassUpdateSchema = Body(...)):
    user_id = system_service.get_current_id(request)
    response = user_class_service.update_user_class(id, user_id, session, body)
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.CREATE,
        type=LOG_TYPE.LOG_USER_CLASS,
        description='Cập nhật lớp đánh dấu',
    ))
    if response:
        return ListResponseSchema(data=response, total_record=1, status=200, message="Cập nhật thành công")
    return {"status": 202,"detail": "cập nhật không thành công"}

@router.delete("/user_class/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def user_class_delete(request: Request, id: int, session: Session = DB):
    user_id = system_service.get_current_id(request)
    response = user_class_service.delete_user_class(user_id, id, session)
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.DELETE,
        type=LOG_TYPE.LOG_USER_CLASS,
        description=f'Xóa lớp đã đánh dấu {id}',
    ))

    return response