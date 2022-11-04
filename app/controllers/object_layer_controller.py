import json
import csv
import pandas as pd
from openpyxl import load_workbook
from io import BytesIO, StringIO
from typing import List, Union
import requests
from databases.db import Session, get_db
from fastapi import FastAPI, Depends, APIRouter, Body, Request, Response,File, Form, UploadFile, HTTPException
from app.models.object_layers import ObjectLayers
from app.services.object_layers import object_layers_service
from app.services.object_layers.schemas.object_layers_schema import ObjectLayersUpdateSchema, ObjectLayersCreateSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system import system_service
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
from app.services.minio.minio_service import MinioService
from config import get_config
router = APIRouter()
TAG = 'Object layer'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/object_layer/list", dependencies=[LOGIN], tags=[TAG])
async def get_all_object_layer(request: Request, session: Session = DB):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_USER_LAYER,
            description='Danh sách lớp của người dùng',
            detail=f'danh sách lớp của người dùng'
        ))

        user_id = system_service.get_current_id(request)
        response = object_layers_service.get_all_by_user_id(session, user_id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

@router.post("/object_layer/create", dependencies=[LOGIN], tags=[TAG])
async def object_layer_create(request: Request, session: Session = DB, body: ObjectLayersCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_USER_LAYER,
            description='Thêm lớp cho người dùng',
            detail=f'thêm lớp cho người dùng {str(body)}'
        ))
        user_id = system_service.get_current_id(request)

        response = object_layers_service.create_object_layer(session, user_id, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm lớp thành công")
        return {"status": 202, "detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))  

@router.put("/object_layer/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def object_layer_update(request: Request, id: int, session: Session = DB, body: ObjectLayersUpdateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)
        response = object_layers_service.update_object_layer(id, user_id, session, body)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_USER_LAYER,
            description='Cập nhật lớp đánh dấu',
            detail=f'cập nhật lớp đánh dấu {str(body)}'
        ))
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Cập nhật thành công")
        return {"status": 202,"detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))  

@router.delete("/object_layer/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def user_class_delete(request: Request, id: int, session: Session = DB):
    try:
        user_id = system_service.get_current_id(request)
        item = object_layers_service.get_object_layer_by_id(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_USER_LAYER,
            description=f'Xóa lớp đã đánh dấu',
            detail=f'xóa lớp đã đánh dấu {str(item.data.__dict__)}'
        ))
        
        response = object_layers_service.delete_object_layer(user_id, id, session)
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))  

@router.get("/object_layer/detail/{id}", dependencies=[LOGIN], tags=[TAG])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        item = object_layers_service.get_object_layer_by_id(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_USER_LAYER,
            description=f'xem chi tiết lớp đã đánh dấu',
            detail=f'xem chi tiết lớp đã đánh dấu {str(item.data.__dict__)}'
        ))
        response = object_layers_service.get_object_layer(session, id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))  

@router.get("/object_layer/get_symbols", dependencies=[LOGIN], tags=[TAG])
async def get_symbols(session: Session = DB):
    bucket_name = get_config("MINIO_BUCKET_NAME")
    object_names = object_layers_service.get_all_symbols(session)
    minio_client = MinioService()
    response = []
    for item in object_names:
        item.url = minio_client.presigned_get_object(bucket_name, item.object_name)
        del item.__dict__['object_name']
        response.append(item)

    return {"status": 200, "data": response}

@router.post("/object_layer/uploadfile/", dependencies=[LOGIN], tags=[TAG])
async def create_file(id: int, request: Request, session: Session = DB, file: UploadFile = File()):
    user_id = system_service.get_current_id(request)
    if id <= 0:
        return {"status": 202, "detail": "Vui lòng kiểm tra lại du lieu"}
    item = session.query(ObjectLayers).filter(ObjectLayers.id == id, ObjectLayers.user_id == user_id).first()
    if not item:
        raise HTTPException(404, detail=f'Chua co lop du lieu vui long kiem tra lai')

    if file.content_type not in ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "application/geo+json"]:
        raise HTTPException(400, detail=file.content_type)

    if file.content_type == 'application/geo+json':
        data = pd.read_json(BytesIO(file.file.read()))
        dataConvert = data.to_dict(orient='records')

        for row in dataConvert:
            if not ('coordinates') in row['features']['geometry']:
                return {"status": 202, "detail": "Vui lòng kiểm tra lại mẫu file. file không đúng định dạng mẫu file"}
            object_layers_service.create_object_by_file_json(session, user_id, id, row['features']['geometry'])

        file.file.close()

    if file.content_type == 'text/csv' or file.content_type == 'application/vnd.ms-excel':
        data = pd.read_csv(BytesIO(file.file.read()))
        dataConvert = data.to_dict(orient='records')
        if file.content_type == 'text/csv' or file.content_type == 'application/vnd.ms-excel':
            for row in dataConvert:
                if not ('WKT' and 'name' and 'description' and 'Lat' and 'Lon') in row:
                    return {"status": 202, "detail": "Vui lòng kiểm tra lại mẫu file. file không đúng định dạng mẫu file"}
                object_layers_service.create_object_by_file_csv(session, user_id, id, row)
            file.file.close()

    if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        data = pd.read_excel(file.file.read())
        dataConvert = data.to_dict(orient='records')
        for row in dataConvert:
            if not 'WKT' in row or not 'name' in row or not 'description' in row or not 'Lat' in row or not 'Lon' in row :
                return {"status": 202, "detail": "Vui lòng kiểm tra lại mẫu file. file không đúng định dạng mẫu file"}
            object_layers_service.create_object_by_file_xlsx(session, user_id, id, row)
        file.file.close()

    response = object_layers_service.get_object_layer(session, id)

    return response

