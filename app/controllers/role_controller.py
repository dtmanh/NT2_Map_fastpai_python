import json
from fastapi import Depends, APIRouter, Path, Body, Request, HTTPException
from pydantic import PositiveInt
from app.services.auth.auth_bearer import JWTBearer
from app.services.roles.schemas.RoleCreateSchema import RoleCreateSchema
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
from databases.db import Session, get_db
from app.services.roles import role_service
from app.services.system_log import system_log_service
from app.services.system import system_service

router = APIRouter()
TAG = 'Role'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/roles/list", dependencies=[LOGIN], tags=[TAG])
async def get_all_roles(request: Request, name_role: str = None, session: Session = DB):
    try:
        if name_role:
            detail=f'xem danh sách nhóm quyền {name_role}'
        else:
            detail=f' xem danh sách tất cả nhóm quyền'
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_PERMISSION,
            description='Danh sách nhóm quyền',
            detail=detail
        ))

        return role_service.getAllRoles(session, name_role)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/roles/create", dependencies=[LOGIN], tags=[TAG])
async def create_new_role(request: Request, session: Session = DB, body: RoleCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_PERMISSION,
            description='Tạo nhóm quyền',
            detail=f' thêm mới một nhóm quyền {body}',
        ))

        return role_service.createNewRole(session, body)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

@router.put("/roles/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def role_update(request: Request, id: int, session: Session = DB, body: RoleCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.UPDATE,
            type=LOG_TYPE.LOG_PERMISSION,
            description='Cập nhật nhóm quyền',
            detail=f' cập nhật nhóm quyền {body}',
        ))

        return role_service.update_role(id, session, body)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

@router.get("/roles/detail/{id}", dependencies=[LOGIN], tags=[TAG])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        log_id = system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_PERMISSION,
            description='Chi tiết nhóm quyền',
             detail=f' xem chi tiết nhóm quyền {id}',
        ))
        role_info = role_service.get_role(session, id)
        if role_info:
            #  update system_log
            detail = f' xem chi tiết nhóm quyền {role_info.data.__dict__}'
            system_log_service.update_log(log_id, session, detail)
        
        return role_service.get_role(session, id)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))       

@router.delete("/roles/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def role_delete(request: Request, id: int, session: Session = DB):
    try:
        response = role_service.delete_role(id, session)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_PERMISSION,
            description=f'Xóa nhóm quyền {id}',
            detail = f' xóa nhóm quyền {id}'
        ))

        # Action system log system_log_create
        return {"status": 200,"detail": "Xóa nhóm quyền {id} thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))       