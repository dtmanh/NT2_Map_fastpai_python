from http.client import HTTPException
import json
from app.schemas.filter_schema import FilterSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.source_data_collection.schemas.source_data_collections_schema import SourceDataCollectionCreateSchema, SourceDataCollectionUpdateSchema
from databases.db import Session, get_db
from app.services.system import system_service
from app.services.source_data_collection import source_data_collection_service
from app.services.auth.auth_bearer import JWTBearer
from fastapi import Depends, APIRouter, Body, Request
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
router = APIRouter()
TAG = 'Nguồn thu nhập dữ liệu'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/source_data_collection/list", dependencies=[LOGIN], tags=[TAG])
def list(request: Request, session: Session = DB, params: FilterSchema = Depends()):
    try:
        user_id = system_service.get_current_id(request)
        params.filter = json.loads(params.filter)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='danh sách nguồn dữ liệu',
            detail=f'danh sách nguồn dữ liệu {str(params)}'
        ))

        response = source_data_collection_service.list(session, user_id, params)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi hệ thống.")

@router.get("/source_data_collection/list_available", dependencies=[LOGIN], tags=[TAG])
def list_available(request: Request, session: Session = DB, params: FilterSchema = Depends()):
    try:
        params.filter = json.loads(params.filter)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='danh sách nguồn dữ liệu có sẵn',
            detail=f'danh sách nguồn dữ liệu có sẵn {str(params)}'
        ))
        response = source_data_collection_service.list_available(session, params)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi hệ thống.")

@router.get("/source_data_collection/{id}", dependencies=[LOGIN], tags=[TAG])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        item = source_data_collection_service.get_detail(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='chi tiết nguồn dữ liệu',
            detail=f'danh sách nguồn dữ liệu có sẵn {str(item.data.__dict__)}'
        ))

        return source_data_collection_service.get_detail(session, id)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err)) 

@router.post("/source_data_collection/create", dependencies=[Depends(JWTBearer())], tags=[TAG])
def create(request: Request, session: Session = DB, body: SourceDataCollectionCreateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='Thêm nguồn dữ liệu',
            detail=f'thêm nguồn dữ liệu {body}'
        ))
        response = source_data_collection_service.create(session, user_id, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm nguồn dữ liệu thành công")

        return {"status": 202, "detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err)) 

@router.put("/source_data_collection/update/{id}", dependencies=[Depends(JWTBearer())], tags=[TAG])
def update(request: Request, id: int, session: Session = Depends(get_db), body: SourceDataCollectionUpdateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='Cập nhật nguồn dữ liệu',
            detail=f'cập nhật nguồn dữ liệu {body}'
        ))
        response = source_data_collection_service.update(id, user_id, session, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Cập nhật thành công")
        return {"status": 202, "detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err)) 

@router.delete("/source_data_collection/delete/{id}", dependencies=[Depends(JWTBearer())], tags=[TAG])
def delete(request: Request, id: int, session: Session = Depends(get_db)):
    try:
        item = source_data_collection_service.get_detail(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='Xóa nguồn dữ liệu',
            detail=f'xóa nguồn dữ liệu {str(item.data.__dict__)}'
        ))

        response = source_data_collection_service.delete(id, session)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err)) 