from typing import List

from fastapi import Depends, APIRouter, Body, Request, Response, HTTPException
from app.services.auth.auth_bearer import JWTBearer
from app.services.auth.auth_service import authenticate_user
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
from databases.db import Session, get_db
from app.services.auth.schemas.auth_schema import UserLoginSchema
from app.services.system_log import system_log_service
from app.services.auth.auth_handle import decodeJWT


router = APIRouter()
TAG = 'Auth'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.post("/auth/login_system", tags=[TAG])
async def login(request: Request, response: Response, session: Session = DB, user: UserLoginSchema = Body(...)):
    try:
        auth = authenticate_user(session, user, True)
        if(auth):
            # region Todo add system log
            detail_log = f"""User: {user.email} đăng nhập vào hệ thống"""
            system_log_service.system_log_create(session, request, OverideSystemLogSchema(
                action=LOG_ACTION.LOGIN,
                type=LOG_TYPE.LOG_MANAGER,
                description= detail_log,
                detail= detail_log,
                access_token=auth.access_token
            ))
            response.set_cookie(key="AccessToken",
                                value=auth.access_token, httponly=True)
        
        return auth
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/auth/login", tags=[TAG])
async def login(request: Request, response: Response, session: Session = DB, user: UserLoginSchema = Body(...)):
    try:
        auth = authenticate_user(session, user, False)
        if(auth):
            # region Todo add system log
            detail_log = f"""User: {user.email} đăng nhập vào website"""
            system_log_service.system_log_create(session, request, OverideSystemLogSchema(
                action=LOG_ACTION.LOGIN,
                type=LOG_TYPE.LOG_MANAGER,
                description= detail_log,
                detail= detail_log,
                access_token=auth.access_token
            ))
            response.set_cookie(key="AccessToken",
                                value=auth.access_token, httponly=True)
            # endregion
        return auth
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err))
        
@router.post("/logout", dependencies=[LOGIN], tags=[TAG])
def logout(request: Request, response: Response, session: Session = DB):
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.LOGOUT,
        type=LOG_TYPE.LOG_MANAGER,
        description='Đăng xuất hệ thống',
    ))

    response.set_cookie(key="AccessToken", value="")
    return True
