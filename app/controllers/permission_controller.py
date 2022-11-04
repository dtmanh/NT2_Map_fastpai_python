import json
from fastapi import Depends, APIRouter, Path, Body, Request, HTTPException
from pydantic import PositiveInt
from app.services.auth.auth_bearer import JWTBearer
from app.services.permissions.schemas.PermissionSchema import PermissionCreateSchema
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
from databases.db import Session, get_db
from app.services.permissions import permission_service
from app.services.system_log import system_log_service
from app.services.system import system_service

router = APIRouter()
TAG = 'Permission'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/permission/list", dependencies=[LOGIN], tags=[TAG])
async def get_all_permission(request: Request, session: Session = DB):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_PERMISSION,
            description='Danh sách quyền hệ thống',
            detail=f' xem danh sách quyền trong hệ thống',
        ))

        return permission_service.getAllRolePermission(session)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/permission/create", dependencies=[LOGIN], tags=[TAG])
async def create_new_permission(request: Request, session: Session = DB, body: PermissionCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_PERMISSION,
            description='Tạo quyền hệ thống',
            detail=f' thêm quyền trong hệ thống {body}',
        ))
        return permission_service.createNewPermission(session, body)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.put("/permission/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def role_update(request: Request, id: int, session: Session = DB, body: PermissionCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.UPDATE,
            type=LOG_TYPE.LOG_PERMISSION,
            description='Cập nhật quyền hệ thống',
            detail=f'cập nhật quyền trong hệ thống {body}',
        ))

        return permission_service.update_permission(id, session, body)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.delete("/permission/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def permission_delete(request: Request, id: int, session: Session = DB):
    try:
        response = system_log_service.delete_user(id, session)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_PERMISSION,
            description=f'Xóa quyền id: {id} trên hệ thống',
            detail=f' xóa quyền trong hệ thống {id}',
        ))

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))