import json
from typing import List, Union
import requests
from databases.db import Session, get_db
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Depends, APIRouter, Body, Request, Response
from app.services.objects import objects_service
from app.services.object_layers import object_layers_service
from app.services.objects.schemas.objects_schema import ObjectCreateSchema, ObjectUpdateSchema, ObjectIDSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system import system_service
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
router = APIRouter()
TAG = 'Object'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/object/list", dependencies=[LOGIN], tags=[TAG])
async def get_all_object(request: Request, session: Session = DB, params: ObjectIDSchema = Depends()):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_USER_LAYER,
            description='Danh sách layer của người dùng',
            detail=f'danh sách layer của người dùng {params}'
        ))

        user_id = system_service.get_current_id(request)
        params.filter = json.loads(params.filter)
        response = objects_service.get_all_by_user_id(session, user_id, params)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))  

@router.post("/object/create", dependencies=[LOGIN], tags=[TAG])
async def object_create(request: Request, session: Session = DB, body: ObjectCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_OBJECT,
            description='Thêm đối tượng cho lớp',
            detail=f'thêm đối tượng cho lớp {body}'
        ))
        user_id = system_service.get_current_id(request)

        # todo is valid content geometry
        system_service.is_valid_geometry_json(body.geometry)

        response = objects_service.create_object(session, user_id, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm đối tượng thành công")

        return {"status": 202, "detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))  

@router.put("/object/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def object_update(request: Request, id: int, session: Session = DB, body: ObjectUpdateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_OBJECT,
            description='Cập nhật đối tượng',
            detail=f'cập nhật đối tượng {body}'
        ))
        # todo is valid content geometry
        system_service.is_valid_geometry_json(body.geometry)
        response = objects_service.update_object(id, user_id, session, body)
        
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Cập nhật thành công")
        return {"status": 202, "detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err)) 

@router.delete("/object/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def user_layer_delete(request: Request, id: int, session: Session = DB):
    try:
        user_id = system_service.get_current_id(request)        
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_OBJECT,
            description=f'Xóa đối tượng {id}',
            detail=f'xóa đối tượng {id}'
        ))
        response = objects_service.delete_object(user_id, id, session)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err)) 

@router.get("/object/detail/{id}", dependencies=[LOGIN], tags=[TAG])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        item = objects_service.get_object_by_id(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_OBJECT,
            description=f'Xóa đối tượng {id}',
            detail=f'xóa đối tượng {str(item.data.__dict__)}'
        ))

        response = objects_service.get_object(session, id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err)) 
