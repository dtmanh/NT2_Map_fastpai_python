from datetime import datetime, timedelta
import math
from platform import architecture
from fastapi import Depends, HTTPException
from sqlalchemy import and_
from app.models.system_log import SystemLog
from app.models.user import User
from app.schemas.filter_schema import FilterSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.auth.auth_handle import decodeJWT
from app.services.elasticsearch.elasticsearch_service import create_document, get_document, get_indexs, create_index, search_documents
from app.services.system_log.schemas.system_log_schema import OverideSystemLogSchema
from app.services.user import user_service
from app.services.system import system_service
from databases.db import Session
from sqlalchemy.orm import load_only


def get_all(db: Session, skip: int = 0, limit: int = 100):
    return db.query(SystemLog).offset(skip).limit(limit).all()

# region Filter system log


def get_filter(db: Session, body: FilterSchema = Depends()):
    queryset = db.query(SystemLog).join(User).with_entities(
        SystemLog.id, SystemLog.action, SystemLog.description, SystemLog.warehouse,
        SystemLog.created_at, User.full_name, User.email)

    if "fetchAll" in body.filter:
        queryset = db.query(SystemLog).join(User).with_entities(
            SystemLog.id, SystemLog.action, SystemLog.description,
            SystemLog.created_at, SystemLog.method, SystemLog.type,
            SystemLog.user_agent, SystemLog.ip, SystemLog.url, SystemLog.accept,
            User.full_name, User.email)

        # get id user by full_name
    if "email" in body.filter:
        queryset = queryset.filter(
            User.email.contains(body.filter["email"]))

    if "action" in body.filter:
        queryset = queryset.filter(SystemLog.action == body.filter["action"])

    if "start_date" in body.filter:
        queryset = queryset.filter(
            SystemLog.created_at >= datetime.strptime(
                body.filter["start_date"], '%Y-%m-%d'))

    if "end_date" in body.filter:
        queryset = queryset.filter(
            SystemLog.created_at <= (datetime.strptime(
                body.filter["end_date"], '%Y-%m-%d') + timedelta(days=1))
        )

    if "warehouse" in body.filter:
        if body.filter["warehouse"] == "None":
            queryset = queryset.filter(
                SystemLog.warehouse == None)
        else:
            queryset = queryset.filter(
                SystemLog.warehouse.contains(body.filter["warehouse"]))

    totalRecord = queryset.count()
    offset = body.page_index * body.page_size

    data = queryset.order_by(SystemLog.created_at.desc()).offset(
        offset).limit(body.page_size).all()

    return ListResponseSchema(status=200,
                              total_record=totalRecord,
                              data=data, message="Get list of system logs")
# endregion


def get_detail(db: Session, id: int):
    # attributes = [i for i in SystemLog.__dict__.keys() if i[:1] != '_']
    # attributes.remove("owner")
    # attributes.append("fullname")

    detail = db.query(SystemLog).filter(SystemLog.id == id).first()
    attributes = [i for i in detail.__dict__.keys() if i[:1] != '_']
    response = {}
    for attr in attributes:
        response[attr] = detail.__dict__[attr]

    user = db.query(User).with_entities(User.full_name, User.email).filter(
        User.id == detail.user_id).first()
    response["full_name"] = user.full_name
    response["email"] = user.email
    return response


# def get_extra_info(request):
#     return {'req': {
#         'url': request.url.path,
#         'headers': {'host': request.headers['host'],
#                     'user-agent': request.headers['user-agent'],
#                     'accept': request.headers['accept']},
#         'method': request.method,
#         'httpVersion': request.scope['http_version'],
#         'originalUrl': request.url.path,
#         'query': {}
#         },
#         'res': {'statusCode': 200, 'body': {'statusCode': 200,
#                    'status': 'OK'}}}

# region Create System Log


def system_log_create(db: Session, request, overideSystemLogSchema: OverideSystemLogSchema):
    if(overideSystemLogSchema.access_token):
        user_login = decodeJWT(overideSystemLogSchema.access_token)
    else:
        user_login = decodeJWT(
            request.headers['authorization'].replace('Bearer ', ''))
    
    if overideSystemLogSchema.action != 'Login':
        user_email = system_service.get_current_email(db, request)
        detail = f"Thông tin chi tiết: User {user_email} {overideSystemLogSchema.detail}"
    else:
        detail = overideSystemLogSchema.detail
    # Todo insert system log
    data = SystemLog(
        user_id=user_login['user_id'],
        action=overideSystemLogSchema.action,
        type=overideSystemLogSchema.type,
        method=request.method,
        url=request.url.path,
        ip=request.client.host,
        user_agent=request.headers['user-agent'],
        accept=request.headers['accept'],
        description=overideSystemLogSchema.description,
        detail=detail,
        warehouse=overideSystemLogSchema.warehouse,
        created_at=datetime.now()
    )
    db.add(data)
    db.commit()
    # db.close()
    db.refresh(data)
    item = db.query(SystemLog).get(data.id)

    return item.id
# endregion

def update_log(id: int, db: Session, detail):
    item = db.query(SystemLog).get(id)
    item.detail = detail
    item.updated_at=datetime.now()
    db.commit()
    db.refresh(item)
    return item

# region Test elasticsearch
def test_elasticsearch():

    return search_documents()
    # return get_document('test_log66', 'systen-log', 1)

    # return create_document('test_log66', 'systen-log', 1)
    # return create_index('test_log66')
    # return get_indexs()
# endregion
