from array import array
import json
from typing import List, Union
import requests
import csv
import pandas as pd
from openpyxl import load_workbook
from io import BytesIO, StringIO
# import geojson
from databases.db import Session, get_db
from fastapi import FastAPI, Depends, APIRouter, Body, Request, Response,File, Form, UploadFile, HTTPException
from fastapi.responses import FileResponse
from app.services.mark_map_area import mark_map_area_service
from app.services.mark_map_area.schemas.mark_map_area_schema import MarkMapAreaCreateSchema, MarkMapAreaUpdateSchema, MissionProfileCreateSchema, MissionProfileUpdateSchema
from app.schemas.respose_schema import ListMarkMapResponseSchema, ListResponseSchema, DetailMarkMapResponseSchema
from app.schemas.filter_schema import FilterSchema
from app.services.auth.auth_bearer import JWTBearer
from app.services.system_log import system_log_service
from app.services.system import system_service
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema

import io
from pathlib import Path  

router = APIRouter()
TAG = 'User Mark Map Area'
TAG_MISSION = 'Mission Profile'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)
# todo list mission profile in backend
@router.get("/mark_map/list_all", response_model=ListResponseSchema, dependencies=[LOGIN], tags=[TAG])
def get_all_mark_map_area(request: Request, session: Session = DB, body: FilterSchema = Depends()): 
    try:
        user_id = mark_map_area_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_MISSION_PROFILE,
            description='Danh sách hồ sơ nhiệm vụ và khu vực',
            detail=f'xem danh sách hồ sơ nhiệm vụ và khu vực {body}'
        ))
        body.filter = json.loads(body.filter)
        response = mark_map_area_service.get_all_map_area(session, user_id, body)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/mark_map/list", response_model=ListMarkMapResponseSchema, dependencies=[LOGIN], tags=[TAG])
def get_all_map(request: Request, session: Session = DB, body: FilterSchema = Depends()): 
    try:
        user_id = mark_map_area_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='Danh sách khu vực đánh dấu',
            detail=f' xem danh sách khu vực đánh dấu {body}'
        ))
        body.filter = json.loads(body.filter)
        response = mark_map_area_service.get_all_by_user_id(session, user_id, body)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.get("/mark_map/detail/{id}", dependencies=[LOGIN], tags=[TAG])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        detail_mark_map = mark_map_area_service.get_mark_map_by_id(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='Chi tiết khu vuc',
            detail=f'xem chi tiết khu vuc {str(detail_mark_map.data.__dict__)}'
        ))
        return mark_map_area_service.get_mark_map(session, id)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/mark_map/create", dependencies=[LOGIN], tags=[TAG])
async def mark_map_create(request: Request, session: Session = DB, body: MarkMapAreaCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='Thêm khu vực đánh dấu',
            detail=f'thêm khu vực đánh dấu {body}'
        ))
        user_id = mark_map_area_service.get_current_id(request)
        # check valid content geometry
        system_service.is_valid_geometry_json(body.geometry)

        response = mark_map_area_service.create_mark_map(session, body, user_id)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thành công")    
        return {"status": 202,"detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.put("/mark_map/update/{id}", dependencies=[LOGIN], tags=[TAG])
async def mark_map_update(request: Request, id: int, session: Session = DB, body: MarkMapAreaUpdateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='Cập nhật khu vực đánh dấu',
            detail=f'cập nhật khu vực đánh dấu {body}'
        ))
        user_id = mark_map_area_service.get_current_id(request)
        # todo is valid content geometry
        system_service.is_valid_geometry_json(body.geometry)

        response = mark_map_area_service.update_mark_map(id, session, body, user_id)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thành công")
        return {"status": 202,"detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.delete("/mark_map/delete/{id}", dependencies=[LOGIN], tags=[TAG])
async def mark_map_area_delete(request: Request, id: int, session: Session = DB):
    try:
        response = mark_map_area_service.delete_mark_map(id, session)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DELETE,
            type=LOG_TYPE.LOG_MARK_AREA,
            description=f'Xóa khu vực đánh dấu {id}',
            detail=f'xóa khu vực đánh dấu {id}'
        ))

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

 # todo list mission profile in backend
@router.get("/mission_profile/list", response_model=ListResponseSchema, dependencies=[LOGIN], tags=[TAG_MISSION])
def get_all_map(request: Request, session: Session = DB, body: FilterSchema = Depends()):
    try:
        user_id = mark_map_area_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_MISSION_PROFILE,
            description='Danh sách hồ sơ nhiệm vụ',
            detail=f'danh sách hồ sơ nhiệm vụ {body}'
        ))
        body.filter = json.loads(body.filter)
        response = mark_map_area_service.get_all_mission_profile(session, user_id, body)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

# todo detail mission profile in backend
@router.get("/mission_profile/detail/{id}", dependencies=[LOGIN], tags=[TAG_MISSION])
def get_detail(request: Request, id: int, session: Session = DB):
    try:
        detail_mark_map =mark_map_area_service.get_mission_profile_by_id(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MISSION_PROFILE,
            description='Chi tiết nhiệm vụ',
            detail=f'chi tiết hồ sơ nhiệm vụ {str(detail_mark_map.data.__dict__)}'
        ))

        return mark_map_area_service.get_mission_profile(session, id)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

# todo create mission profile in backend
@router.post("/mission_profile/create", dependencies=[LOGIN], tags=[TAG_MISSION])
async def mission_profile_create(request: Request, session: Session = DB, body: MissionProfileCreateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.CREATE,
            type=LOG_TYPE.LOG_MISSION_PROFILE,
            description='Thêm nhiệm vụ',
            detail=f'thêm hồ sơ nhiệm vụ {body}'
        ))
        user_id = mark_map_area_service.get_current_id(request)

        # todo is valid content geometry
        system_service.is_valid_geometry_json(body.geometry)

        response = mark_map_area_service.create_mission_profile(session, body, user_id)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thành công")

        return {"status": body,"detail": "Không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/mission_profile/update/{id}", dependencies=[LOGIN], tags=[TAG_MISSION])
async def mission_profile_update(request: Request, id: int, session: Session = DB, body: MissionProfileUpdateSchema = Body(...)):
    try:
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.UPDATE,
            type=LOG_TYPE.LOG_MISSION_PROFILE,
            description='Cập nhật nhiệm vụ',
            detail=f'cập nhật hồ sơ nhiệm vụ {body}'
        ))
        user_id = mark_map_area_service.get_current_id(request)
        # todo is valid content geometry
        system_service.is_valid_geometry_json(body.geometry)

        response = mark_map_area_service.update_mission_profile(id, session, body, user_id)
        if response:
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thành công")
        return {"status": 202,"detail": "cập nhật không thành công"}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.delete("/mission_profile/delete/{id}", dependencies=[LOGIN], tags=[TAG_MISSION])
async def mission_profile_delete(request: Request, id: int, session: Session = DB):
    try:
        detail_mark_map =mark_map_area_service.get_mission_profile_by_id(session, id)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.DETAIL,
            type=LOG_TYPE.LOG_MISSION_PROFILE,
            description=f'Xóa nhiệm vụ {id}',
            detail=f'xóa hồ sơ nhiệm vụ {str(detail_mark_map.data.__dict__)}'
        ))
        response = mark_map_area_service.delete_mission_profile(id, session)
        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

  # todo Fillter by mission profile
@router.get("/mission_profile/filter", dependencies=[LOGIN], tags=[TAG_MISSION])
def get_filter_mission(request: Request, session: Session = DB, body: FilterSchema = Depends()):
    try:
        user_id = mark_map_area_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.LIST,
            type=LOG_TYPE.LOG_MARK_AREA,
            description='Lọc ho so nhiem vu',
            detail=f'lọc hồ sơ nhiệm vụ {body}'
        ))
        body.filter = json.loads(body.filter)
        response = mark_map_area_service.get_filter_mission_profile(session, user_id, body)

        return response
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

@router.post("/mission_profile/uploadfile/", dependencies=[LOGIN], tags=[TAG_MISSION])
async def create_file(request: Request, session: Session = DB, file: UploadFile = File()):
    if file.content_type not in ["text/csv", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"]:
        raise HTTPException(400, detail=f'Vui lòng kiểm tra lại mẫu file. file không đúng định dạng mẫu file')

    coordinates = []
    if file.content_type == 'text/csv' or file.content_type == 'application/vnd.ms-excel':
        data = pd.read_csv(BytesIO(file.file.read()))
        dataConvert = data.to_dict(orient='records')
        for row in dataConvert:
            char_to_replace = {'POLYGON ': '', '(': '', ')': ''}
            dataConvert[0]['WKT'] = dataConvert[0]['WKT'].replace('(', '')
            dataConvert[0]['WKT'] = dataConvert[0]['WKT'].replace(')', '')
            kq = dataConvert[0]['WKT'].split()
            if not 'WKT' in row or kq[0] == "POINT":
                coordinates = [float(kq[1]), float(kq[2])]
                raise HTTPException(400, detail=f'Vui lòng kiểm tra lại mẫu file. file không đúng định dạng mẫu file')
            if kq[0] == "POLYGON":
                for key, value in char_to_replace.items():
                    points = dataConvert[0]['WKT'].replace(key, value)
                points = points.replace('POLYGON ', '')
                for item in points.split(','):
                    point = item.split()
                    coordinates.append([float(point[0]),float(point[1])])
                break
        file.file.close()

    if file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        data = pd.read_excel(file.file.read())
        dataConvert = data.to_dict(orient='records')
        for row in dataConvert:
            if not 'WKT' in row or row['WKT'] == "POINT" or row['Polygon'] == '':
                raise HTTPException(400, detail=f'Vui lòng kiểm tra lại mẫu file. file không đúng định dạng mẫu file')
            if row['Polygon']:
                row['Polygon'] = row['Polygon'].replace('(', '')
                row['Polygon'] = row['Polygon'].replace(')', '')
            for item in row['Polygon'].split(','):
                point = item.split()
                coordinates.append([float(point[0]), float(point[1])])
            file.file.close()
            break
    return ListResponseSchema(data=coordinates, total_record=1, status=200, message="Thành công")


@router.get("/mission_profile/exportfile/", dependencies=[LOGIN], tags=[TAG_MISSION])
async def export_file(request: Request, session: Session = DB, body: FilterSchema = Depends()):
    user_id = mark_map_area_service.get_current_id(request)
    system_log_service.system_log_create(session, request, OverideSystemLogSchema(
        action=LOG_ACTION.EXPORT,
        type=LOG_TYPE.LOG_MISSION_PROFILE,
        description='Export danh sách hồ sơ nhiệm vụ và khu vực',
        detail=f'export danh sách hồ sơ nhiệm vụ và khu vực {body}'
    ))
    body.filter = json.loads(body.filter)
    datas = mark_map_area_service.export_excel_map_area(session, user_id, body)
    list = []
    for row in datas:
        list.append([row.name,row.code,row.type,row.user_email,row.geometry])

    df = pd.DataFrame(data=list, columns=["Name", "Code", "Type", "Email", "Geometry"])

    if "file" in body.filter:
        if body.filter['file'] == 'csv':
            media_type = 'application/csv'
            filename = 'hosokhuvuc.csv' 
            filepath = Path('export/csv/hosokhuvuc.csv')  
            filepath.parent.mkdir(parents=True, exist_ok=True)  
            df.to_csv(filepath)    
        elif body.filter['file'] == 'application/xlsx':
            media_type = 'application/xlsx'
            filepath = Path('export/xlsx/hosokhuvuc.xlsx')  
            filename = 'hosokhuvuc.xlsx' 
            filepath.parent.mkdir(parents=True, exist_ok=True)  
            df.to_excel(filepath, index=False)  
    else:
        media_type = 'application/xlsx'
        filepath = Path('export/xlsx/hosokhuvuc.xlsx')  
        filename = 'hosokhuvuc.xlsx' 
        filepath.parent.mkdir(parents=True, exist_ok=True)  
        df.to_excel(filepath, index=False)  

    return FileResponse(path=filepath, filename=filename, media_type=media_type) 

