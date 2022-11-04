import time
from fastapi import FastAPI, Depends, Request
from app.services.auth.auth_handle import decodeJWT
from fastapi.responses import JSONResponse
from app.services.roles_permissions import role_permission_service
from sqlalchemy.orm import Session

async def Check_role(request: Request, call_next):

    if 'authorization' in request.headers:
        user_login = decodeJWT(
            request.headers['authorization'].replace('Bearer ', ''))
        if user_login['expires'] <= time.time():
            return JSONResponse({"detail": "thoi gian truy cap het hang vui long dang nhap lai"})
        # if todo check permission role
        check = False
        if user_login['role_id']:
            action = role_permission_service.get_action_role_permission(Session(), user_login['role_id'])
            list_action = request.url.path.split('/')
            for item in action:
                if item['permission_module'] == list_action[2] and item['permission_key'] == list_action[3]:
                    check = True
        if check == False:
            content = {"status": 201, "message": "You do not have access"}
            response = JSONResponse(content=content)
            return response

    response = await call_next(request)

    return response
