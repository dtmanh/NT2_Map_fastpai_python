import json
from typing import List, Union
import requests
from app.services.equipments.schemas.equipments_schema import EquipmentCreateSchema, EquipmentIDSchema, EquipmentUpdateSchema
from databases.db import Session, get_db
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Depends, APIRouter, Body, Request, Response
from app.services.equipments import equipments_service
from app.schemas.respose_schema import ListResponseSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system import system_service
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
router = APIRouter()
TAG = 'Equipments'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

# danh sach trang thiet bi trong quan tri admin
@router.get("/equipment/list", dependencies=[LOGIN], tags=[TAG])
async def get_all_equipments(request: Request, session: Session = DB, params: EquipmentIDSchema = Depends()):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_EQUIPMENT,
            description='Danh sách trang thiết bị của người dùng',
            detail=f'danh sách trang thiết bị của người dùng {str(params)}'
        ))

        user_id = system_service.get_current_id(request)
        params.filter = json.loads(params.filter)
        response = equipments_service.get_all_equipments(session, params)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/equipment/create", dependencies=[LOGIN], tags=[TAG])
async def equipment_create(request: Request, session: Session = DB, body: EquipmentCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_EQUIPMENT,
            description='Thêm trang thiết bị',
            detail=f'thêm trang thiết bị {body}'
        ))
    
        response = equipments_service.create_equipment(session, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm trang thiết bị thành công")

        return {"status": 202, "detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.put("/equipment/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def equipment_update(request: Request, id: int, session: Session = DB, body: EquipmentUpdateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_EQUIPMENT,
            description='Cập nhật trang thiết bị',
            detail=f'cập nhật trang thiết bị {body}'
        ))
        response = equipments_service.update_equipments(id, session, body)
        if response:
            return response
        return {"status": 202, "detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.delete("/equipment/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def delete_equipments(request: Request, id: int, session: Session = DB):
    try:
        item = equipments_service.get_detail(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_EQUIPMENT,
            description=f'Xóa trang thiết bị {id}',
            detail=f'xóa trang thiết bị {str(item.data.__dict__)}'
        ))
        response = equipments_service.delete_equipments(id, session)
        if response:
            return {"status": 200, "detail": "Xóa trang thiết bị thành công"}

        return {"status": 202, "detail": "Xóa trang thiết bị không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/equipment/detail/{id}", dependencies=[LOGIN], tags=[TAG])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        response = equipments_service.get_detail(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_EQUIPMENT,
            description=f'Xem chi tiết trang thiết bị {id}',
            detail=f'xem chi tiết trang thiết bị {str(response.data.__dict__)}'
        ))
        return equipments_service.get_detail(session, id)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))