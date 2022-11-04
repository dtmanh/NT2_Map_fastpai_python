import json
from typing import List

from fastapi import Depends, APIRouter, Body, HTTPException, Request, status
from app.models.user import User
from app.schemas.filter_schema import FilterSchema
from app.schemas.respose_schema import ListResponseSchema, ResultResponseSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
from databases.db import Session, get_db
from app.services.user import user_service
from app.services.system_log import system_log_service
from app.services.system.system_service import get_current_id
from app.services.user.schemas.user_create_schema import UserCreateSchema, UserUpdateSchema, UserResetPasswordSchema

router = APIRouter()
TAG = 'Users'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

""" 
    description: Danh sach tai khoan user
    params: page_size: int = 10, page_index: int = 0; filter: object = {"keyword":"...","active":True,"role_id":"..."}
    return: status: 200, total_record: int, message:"", data: {}
 """
@router.get( "/user/list", response_model=ListResponseSchema, tags=[TAG], response_model_exclude={},dependencies=[LOGIN],)
def get_all(request: Request, session: Session = DB, body: FilterSchema = Depends()):
    try:
        body.filter = json.loads(body.filter)
        detail = user_service.detail_log(session, request,body)  
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.SEARCH,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Danh sách thành viên',
            detail=f' xem chi tiết thành viên {detail}',
        ))
        response = user_service.get_all(session, body)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))


@router.get("/user/detail/{id}", dependencies=[LOGIN], tags=[TAG])
async def get_detail(request: Request, id: int, session: Session = DB):
    try:
        log_id = system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.SEARCH,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Chi tiết thành viên',
            detail=f'xem chi tiết thành viên {id}',
        ))
        
        user_info = user_service.get_user(session, id)
        if user_info:
            #  update system_log
            detail = f'xem chi tiết thành viên {user_info.data.__dict__}'
            system_log_service.update_log(log_id, session, detail)
        response = user_service.get_user(session, id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/user/create", response_model=ResultResponseSchema, dependencies=[LOGIN], tags=[TAG])
async def user_create(request: Request, session: Session = DB, body: UserCreateSchema = Body(...)):
    try:
        log_id =  system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_MANAGER,
            description='Tạo mới thành viên',
            detail = f' tạo mới thành viên {body}'
        ))
        response = user_service.create_user(session, body)
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.put("/user/update/{id}", response_model=ResultResponseSchema, dependencies=[LOGIN], tags=[TAG])
async def user_update(request: Request, id: int, session: Session = DB, body: UserUpdateSchema = Body(...)):
    try:
        # Action system log system_log_create
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.UPDATE,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Cập nhật thông tin thành viên {id}',
            detail=f'cập nhật thông tin thành viên {body}'
        ))
        response = user_service.update_user(id, session, body)
        
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.delete("/user/delete/{id}", response_model=ResultResponseSchema, dependencies=[LOGIN], tags=[TAG])
async def user_delete(request: Request, id: int, session: Session = DB):
    try:
        # Action system log system_log_create
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Xóa thành viên {id}',
            detail=f' Xóa thành viên {id}'
        ))
        response = user_service.delete_user(id, session)        
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/user/info", response_model=ResultResponseSchema, dependencies=[LOGIN], tags=[TAG])
def get_user_info(request: Request, session: Session = DB):
    try:
        user_id = get_current_id(request)
        # Action system log system_log_create
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Xem thông tin chi tiết thành viên {user_id}',
            detail=f'xem thông tin chi tiết thành viên {user_id}'
        ))

        response = user_service.get_user(session, user_id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.put("/user/reset_password/{id}", response_model=ResultResponseSchema, dependencies=[LOGIN], tags=[TAG])
async def user_reset_password(request: Request, id: int, session: Session = DB, body: UserResetPasswordSchema = Body(...)):
    try:
        # Action system log system_log_create
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.RESET_PASSWORD,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Thay đổi mật khẩu thành viên',
            detail=f'thay đổi mật khẩu thành viên {id}'
        ))
        
        response = user_service.reset_password(session, id, body)
        
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    