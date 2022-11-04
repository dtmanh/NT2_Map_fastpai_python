import json
from typing import List
from fastapi import Body, Depends, APIRouter, Request, UploadFile, HTTPException
from app.services.auth.auth_bearer import JWTBearer
from app.services.minio.minio_service import MinioService
from app.services.minio.schemas.CopySchema import CopySchema, ListCopySchema
from app.services.minio.schemas.CreateFolderSchema import CreateFolderSchema
from ..services.minio.schemas.DeleteSchema import DeleteSchema
from app.services.minio.schemas.GetListChildren import GetListChildrenSchema
from ..services.minio.schemas.OptionEnum import OptionEnum
from app.services.system_log import system_log_service
from app.services.system import system_service
from databases.db import Session, get_db
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema

router = APIRouter()
TAG = 'MinIO'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.get("/minio/list", dependencies=[LOGIN], tags=[TAG])
async def list(request: Request, session: Session = DB, params: GetListChildrenSchema = Depends()):
    try:
        log_id = system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Danh sách thư mục lưu trữ',
            detail=f' xem danh sách thư mục lưu trữ {params}',
        ))

        minio_client = MinioService()
        objects = minio_client.list_all_sub_directories(params)
        return objects
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/minio/move",  dependencies=[LOGIN], tags=[TAG])
async def move(request: Request, session: Session = DB, body: ListCopySchema = Body(...)):
    try:
        log_id = system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.MOVE,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Di chuyển thư mục lưu trữ',
            detail=f'di chuyển thư mục lưu trữ {body}',
        ))

        data = body.data
        srcWarehouse = data[0].sourcePath.split('/')[0]
        dstWarehouse = data[0].destinationPath.split('/')[0]

        warehouse = srcWarehouse
        if srcWarehouse != dstWarehouse:
            warehouse += ", " + dstWarehouse

        description = ""
        minio_client = MinioService()
        response = {}

        if body.type == OptionEnum.OBJECT:
            srcPath = "/".join(data[0].sourcePath.split('/')[:-1])
            dstPath = "/".join(data[0].destinationPath.split('/')[:-1])
            description = f'Di chuyển file từ {srcPath} đến {dstPath}'
            response = minio_client.move_objects(data)

        else:
            srcPath = data[0].sourcePath
            dstPath = "/".join(data[0].destinationPath.split('/')[:-1])
            description = f'Di chuyển folder từ {srcPath} đến {dstPath}'
            response = minio_client.move_folder(
                data[0].sourcePath, data[0].destinationPath)

        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.EDIT,
            type=LOG_TYPE.LOG_MANAGER,
            description=description,
            warehouse=warehouse
        ))
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/minio/delete", dependencies=[LOGIN], tags=[TAG])
async def delete(request: Request, body: DeleteSchema = Body(...), session: Session = DB):
    try:
        log_id = system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Xóa thư mục lưu trữ',
            detail=f'xóa thư mục lưu trữ {body}',
        ))

        minio_client = MinioService()
        description = ""
        warehouse = body.data[0].split("/")[0]

        if body.type == OptionEnum.FOLDER:
            minio_client.remove_folder(body.data[0])
            description = 'Xóa folder'
        else:
            for file in body.data:
                minio_client.remove_file(file)
            description = "Xóa files"

        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_MANAGER,
            description=description,
            warehouse=warehouse
        ))
        return True
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/minio/statistic", dependencies=[LOGIN], tags=[TAG])
async def get_statistic(warehouse: str):
    minio_client = MinioService()
    response = minio_client.get_statistics(warehouse)
    return response


@router.post("/minio/create", dependencies=[LOGIN], tags=[TAG])
async def create_folder(request: Request, body: CreateFolderSchema = Body(...), session: Session = DB):
    try:
        folder_path = body.folder_path
        minio_client = MinioService()
        response = minio_client.create_folder(folder_path)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Tạo thư mục {folder_path}',
            detail=f'tạo thư mục lưu trữ {body}',
            warehouse=folder_path.split('/')[0]
        ))
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/minio/uploadfile/", dependencies=[LOGIN], tags=[TAG])
async def create_upload_file(request: Request, file_list: List[UploadFile], folder: str, session: Session = DB):
    try:
        responses = []
        minio_client = MinioService()
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_MANAGER,
            description=f'Upload file ',
            detail=f' up load file {file_list} vào thư mục lưu trữ {folder}',
        ))

        for file in file_list:
            response = minio_client.create_object(file, folder)
            responses.append(response)
            # responses.append(file.__dict__)
        
        return responses
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))