import json
from typing import List, Union
import requests
from app.services.object_equipments.schemas.object_equipments_schema import ObjectEquipmentCreateSchema, ObjectEquipmentIDSchema, ObjectEquipmentUpdateSchema
from databases.db import Session, get_db
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Depends, APIRouter, Body, Request, Response
from app.services.object_equipments import object_equipments_service
from app.schemas.respose_schema import ListResponseSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system import system_service
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
router = APIRouter()
TAG = 'Object Equipment'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

# danh sach trang thiet bi cua doi tuong
@router.get("/object_equipment/object/{id}", dependencies=[LOGIN], tags=[TAG])
async def get_equipments_by_object(request: Request, id: int, session: Session = DB):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_OBJECT_EQUIPMENT,
            description='Danh sách trang thiết bị của người dùng',
            detail=f'danh sách trang thiết bị của người dùng {id}'
        ))
        response = object_equipments_service.get_all_equiqments(session, id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/object_equipment/object_left/{id}", dependencies=[LOGIN], tags=[TAG])
async def get_equiqments_left_by_object(request: Request, id: int, session: Session = DB):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_OBJECT_EQUIPMENT,
            description='Danh sách trang thiết bị của người dùng',
            detail=f'danh sách trang thiết bị của người dùng {id}'
        ))

        response = object_equipments_service.get_all_equipments_left(session, id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))


@router.post("/object_equipment/create", dependencies=[LOGIN], tags=[TAG])
async def object_equipment_create(request: Request, session: Session = DB, body: ObjectEquipmentCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_OBJECT_EQUIPMENT,
            description='Thêm trang thiết bị cho đối tượng',
            detail=f'thêm trang thiết bị cho đối tượng {body}'
        ))
    
        response = object_equipments_service.create_object_equipment(session, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm trang thiết bị cho đối tượng thành công")

        return {"status": 202, "detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.put("/object_equipment/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def equipment_update(request: Request, id: int, session: Session = DB, body: ObjectEquipmentUpdateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_OBJECT_EQUIPMENT,
            description='Cập nhật trang thiết bị cho đối tượng',
            detail=f'cập nhật trang thiết bị cho đối tượng {body}'
        ))
        response = object_equipments_service.update_object_equipment(id, session, body)
        if response:
            return response
        return {"status": 202, "detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))      

@router.delete("/object_equipment/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def delete_object_equipments(request: Request, id: int, session: Session = DB):
    try:
        item = object_equipments_service.get_detail(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_OBJECT_EQUIPMENT,
            description=f'Xóa trang thiết bị {id}',
            detail=f'xóa trang thiết bị của người dùng {str(item.data.__dict__)}'
        ))
        response = object_equipments_service.delete_object_equipments(id, session)
        if response:
            return {"status": 200, "detail": "Xóa trang thiết bị thành công"}

        return {"status": 202, "detail": "Xóa trang thiết bị không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))      

@router.get("/object_equipment/detail/{id}", dependencies=[LOGIN], tags=[TAG])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        item = object_equipments_service.get_detail(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_OBJECT_EQUIPMENT,
            description=f'Xóa trang thiết bị {id}',
            detail=f'xóa trang thiết bị của người dùng {str(item.data.__dict__)}'
        ))
        response = object_equipments_service.get_detail(session, id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    