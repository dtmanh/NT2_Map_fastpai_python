import json
from typing import List, Union
import requests
from fastapi import FastAPI
from databases.db import Session, get_db
from fastapi import Depends, APIRouter, Body, Request, Response, HTTPException
from app.services.user_layer import user_layer_service
from app.services.user_layer.schemas.user_layer_schema import UserLayerCreateSchema, UserLayerUpdateSchema, UserLayerIDSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system import system_service
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
router = APIRouter()
TAG = 'User Layer'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/user_layer/list", dependencies=[LOGIN], tags=[TAG])
async def get_all_layer(request: Request, session: Session = DB, params: UserLayerIDSchema = Depends()):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_USER_LAYER,
            description='Danh sách layer của người dùng',
            detail=f'Danh sách layer của người dùng {params}'
        ))

        user_id = system_service.get_current_id(request)
        response = user_layer_service.get_all_by_user_id(session, user_id, params)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

@router.post("/user_layer/create", dependencies=[LOGIN], tags=[TAG])
async def user_layer_create(request: Request, session: Session = DB, body: UserLayerCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_USER_LAYER,
            description='Thêm đánh dấu layer cho người dùng',
            detail=f'Thêm đánh dấu layer cho người dùng {body}'
        ))
        user_id = system_service.get_current_id(request)

        check_user_layer = user_layer_service.check_user_layer_id(session, user_id, body.layer_id)
        if check_user_layer:
            return ListResponseSchema(data=check_user_layer, total_record=1, status=404, message="Layer đã tồn tại")

        # todo is valid content geometry
        system_service.is_valid_geometry_json(body.geometry)

        response = user_layer_service.create_user_layer(session, user_id, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm layer thành công")
        return {"status": 202, "detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))   

@router.put("/user_layer/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def user_layer_update(request: Request, id: int, session: Session = DB, body: UserLayerUpdateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)

        # todo is valid content geometry
        system_service.is_valid_geometry_json(body.geometry)

        response = user_layer_service.update_user_layer(id, user_id, session, body)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_USER_LAYER,
            description='Cập nhật layer đánh dấu',
            detail=f'cập nhật layer đánh dấu {body}'
        ))
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Cập nhật thành công")
        return {"status": 202,"detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))   

@router.delete("/user_layer/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def user_layer_delete(request: Request, id: int, session: Session = DB):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_USER_LAYER,
            description=f'Xóa layer đã đánh dấu {id}',
            detail=f'xóa layer đã đánh dấu {id}'
        ))
        response = user_layer_service.delete_user_layer(user_id, id, session)
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))   