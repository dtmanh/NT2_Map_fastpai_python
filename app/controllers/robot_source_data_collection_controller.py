from http.client import HTTPException
import json
from app.schemas.filter_schema import FilterSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.robot_source_data_collection.schemas.robot_source_data_collections_schema import ListRobotSourceDataCollectionSchema, RobotSourceDataCollectionCreateSchema, RobotSourceDataCollectionUpdateSchema
from app.services.source_data_collection.schemas.source_data_collections_schema import SourceDataCollectionCreateSchema, SourceDataCollectionUpdateSchema
from databases.db import Session, get_db
from app.services.system import system_service
from app.services.robot_source_data_collection import robot_source_data_collection_service
from app.services.auth.auth_bearer import JWTBearer
from fastapi import Depends, APIRouter, Body, Request
from app.services.system_log import system_log_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
router = APIRouter()

TAG = 'Robot thu nhập dữ liệu'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)


@router.get("/robot_source_data_collection/list", dependencies=[LOGIN], response_model=ListRobotSourceDataCollectionSchema, tags=[TAG])
def list(request: Request, session: Session = DB, params: FilterSchema = Depends()):
    try:
        params.filter = json.loads(params.filter)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_SOUCE_DATA_COLLECTION,
            description='Danh sách cấu hình',
            detail=f'danh sách cấu hình {params}'
        ))
        response = robot_source_data_collection_service.list(session, params)
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/robot_source_data_collection/{id}", dependencies=[LOGIN], tags=[TAG])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_SOUCE_DATA_COLLECTION,
            description='Chi tiết cấu hình',
            detail=f'chi tiết cấu hình {id}'
        ))
        response = robot_source_data_collection_service.get_detail(session, id)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/robot_source_data_collection/create", dependencies=[LOGIN], tags=[TAG])
def create(request: Request, session: Session = DB, body: RobotSourceDataCollectionCreateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_SOUCE_DATA_COLLECTION,
            description='Tạo nguồn dữ liệu',
            detail=f'tạo nguồn dữ liệu {body}'
        ))
        response = robot_source_data_collection_service.create(session, user_id, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thêm robot nguồn dữ liệu thành công")

        return {"status": 202, "detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.put("/robot_source_data_collection/update/{id}", dependencies=[LOGIN], tags=[TAG])
def update(request: Request, id: int, session: Session = DB, body: RobotSourceDataCollectionUpdateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.UPDATE,
            type=LOG_TYPE.LOG_SOUCE_DATA_COLLECTION,
            description='Cập nhật nguồn dữ liệu',
            detail=f'cập nhật nguồn dữ liệu {body}'
        ))
        response = robot_source_data_collection_service.update(id, user_id, session, body)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Cập nhật thành công")
        return {"status": 202, "detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.delete("/robot_source_data_collection/delete/{id}", dependencies=[LOGIN], tags=[TAG])
def delete(request: Request, id: int, session: Session = DB):
    try:
        user_id = system_service.get_current_id(request)
        item = robot_source_data_collection_service.get_detail(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_SOUCE_DATA_COLLECTION,
            description='Xóa nguồn dữ liệu',
            detail=f'xóa nguồn dữ liệu {str(item.data.__dict__)}'
        ))
        response = robot_source_data_collection_service.delete(id, session)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))