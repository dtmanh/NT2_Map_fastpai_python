from typing import List, Union
import requests
import json
from fastapi import FastAPI
from fastapi import Depends, APIRouter, Body, Request, HTTPException
from app.services.satellite.satellite_handle import TokenVendor
from config import get_config
from fastapi.responses import JSONResponse
from app.schemas.filter_schema import FilterSchema
from app.services.system import system_service
from app.services.auth.auth_bearer import JWTBearer
from app.services.satellite import satellite_service
from app.models.history_search import HistorySearch
from app.services.satellite.schemas.HistorySearch_schema import HistorySearchCreateSchema
from app.services.satellite.schemas.fillter_search_schema import FillterSearchCreateSchema
from databases.db import Session, get_db
from app.services.system_log.schemas.system_log_schema import LOG_ACTION, LOG_TYPE, OverideSystemLogSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.system_log import system_log_service
from app.services.system import system_service

router = APIRouter()
TAG = 'Satellite'
LOGIN = Depends(JWTBearer())
DB = Depends(get_db)

@router.post("/satellite/search", dependencies=[LOGIN], tags=[TAG])
async def get_data(request: Request, session: Session = DB, body: FilterSchema  = Body(...)):
    try:
        body.filter = body.filter
        token = TokenVendor()
    
        api_get_data = get_config('API3')
        data = body.filter
        # data2 = {
        #     "geometry": {
        #         "type": "Polygon",
        #         "coordinates": [
        #             [
        #                 [112.27958679199219, 16.787449898410646],
        #                 [112.38807678222655, 16.787449898410646],
        #                 [112.38807678222655, 16.884717558745834],
        #                 [112.27958679199219, 16.884717558745834],
        #                 [112.27958679199219, 16.787449898410646]
        #             ]
        #         ]
        #     },
        #     "cloud_cover__lte": 0.5,
        #     "cloud_cover__gte": 0,
        #     "item_types": "PSScene3Band,SkySatCollect",
        #     "date__lte": "20200101",
        #     "date__gte": "20200101"    
        # }
        offset = body.page_index * body.page_size
        url = api_get_data + '?limit=%d&offset=%d' % (body.page_size, offset)

        response = requests.post(url=url, json= data, headers={'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'})
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.SEARCH,
            type=LOG_TYPE.LOG_SATELLITE_SEARCH,
            description=f'Tìm kiếm ảnh vệ tinh',
            detail=f' tìm kiếm ảnh vệ tinh {body}',
        ))

        return response.json()
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

@router.post("/satellite/add_history_search", dependencies=[LOGIN], tags=[TAG])
async def create_history_search(request: Request, session: Session = DB, body: HistorySearchCreateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.ADD_SEARCH_HISTORY,
            type=LOG_TYPE.LOG_SATELLITE_SEARCH,
            description=f'lưu thông tin tìm kiếm ảnh vệ tinh',
            detail=f' lưu thông tin tìm kiếm ảnh vệ tinh {body}',
        ))

        return satellite_service.CreateNewHistorySearch(user_id, session, body)
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

@router.get("/satellite/history_search_view", dependencies=[LOGIN], tags=[TAG])
async def get_history_search_view(request: Request, session: Session = DB, page_size: int = 10, page_index: int = 0):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.SEARCH_HISTORY,
            type=LOG_TYPE.LOG_SATELLITE_SEARCH,
            description=f'xem lịch sử ảnh vệ tinh',
            detail=f' xem lịch sử ảnh vệ tinh',
        ))

        data = satellite_service.get_data(session, user_id, page_size, page_index)
        for i in data:
            i.data_search = json.loads(i.data_search)

        return {"data": list(data)}
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

@router.post("/satellite/update_fillter", dependencies=[LOGIN], tags=[TAG])
async def create_fillter(request: Request, session: Session = DB, body: FillterSearchCreateSchema = Body(...)):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.UPDATE_FILLTER_SEARCH,
            type=LOG_TYPE.LOG_SATELLITE_SEARCH,
            description=f'lưu cấu hình tìm kiếm ảnh vệ tinh',
            detail=f' lưu cấu hình tìm kiếm ảnh vệ tinh {body}'
        ))

        item = satellite_service.GetFillterSearch_by_user_id(user_id, session)
        if item:
            response = satellite_service.UpdateFillterSearch(item.id, session, body)
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thành công")
        else:
            response = satellite_service.CreateNewFillterSearch(user_id, session, body)
            return ListResponseSchema(data=response, total_record=1, status=200, message="Thành công")
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))  

@router.get("/satellite/get_filter", dependencies=[LOGIN], tags=[TAG])
def get_filter(request: Request, session: Session = DB):
    try:
        user_id = system_service.get_current_id(request)
        system_log_service.system_log_create(session, request, OverideSystemLogSchema(
            action=LOG_ACTION.GET_FILLTER_SEARCH,
            type=LOG_TYPE.LOG_SATELLITE_SEARCH,
            description=f'lấy thông tin cấu hình tìm kiếm ảnh vệ tinh',
            detail=f' lấy thông tin cấu hình tìm kiếm ảnh vệ tinh'
        ))

        response = satellite_service.GetFillterSearch_by_user_id(user_id, session)
        total = 0
        if response:
            total = 1
            response.data_fillter = json.loads(response.data_fillter)

        return ListResponseSchema(data=response, total_record=total, status=200, message="Thành công")
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))  

@router.get("/satellite/render_token", tags=[TAG])
async def get_token():
    return TokenVendor()