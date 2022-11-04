import json
from typing import List
from fastapi import HTTPException
from sqlalchemy import or_
from sqlalchemy.sql import text
import sqlalchemy
from app.schemas.respose_schema import ListResponseSchema, DetailMarkMapResponseSchema, ResultResponseSchema
from app.services.mark_map_area.schemas.mark_map_area_schema import MarkMapAreaCreateSchema, MarkMapAreaUpdateSchema, MarkMapListSchema, MissionProfileUpdateSchema, MissionProfileCreateSchema
from databases.db import Session
from datetime import datetime
from app.models.user import User
from app.models.mark_map_area import MarkMapArea
from app.services.auth.auth_handle import decodeJWT
from app.schemas.filter_schema import FilterSchema
from app.services.system_log.schemas.system_log_schema import MAP_TYPE
from app.services.system import system_service
def get_all_by_user_id(db: Session, user_id, body: FilterSchema):
    try:
        data = db.query(MarkMapArea).filter(MarkMapArea.user_id == user_id, MarkMapArea.type == MAP_TYPE.AREA)
        if "start_date" in body.filter:
            data = data.filter(MarkMapArea.created_at >= body.filter['start_date'])
        if "end_date" in body.filter:
            data = data.filter(MarkMapArea.created_at <= body.filter['end_date'])
        if "area_id" in body.filter:
            data = data.filter(MarkMapArea.id == body.filter['area_id'])
        if "name" in body.filter:
            data = data.filter(MarkMapArea.name.contains(body.filter['name']))
        if "code" in body.filter:
            data = data.filter(MarkMapArea.code.contains(body.filter['code']))
        if "active" in body.filter:
            data = data.filter(MarkMapArea.active == body.filter['active'])
        # if "user_ids" in body.filter:
        #     data = data.filter(MarkMapArea.user_ids.contains(body.filter['user_ids']))
        total_record = data.count()
        offset = body.page_index * body.page_size
        data = data.order_by(MarkMapArea.created_at.desc()).offset(offset).limit(
            body.page_size).all()
        for i in data:
            if i.properties:
                i.properties = json.loads(i.properties)
            if i.geometry:
                i.geometry = json.loads(i.geometry)
            if i.meta_data:
                i.meta_data = json.loads(i.meta_data)

        return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi hệ thống.")

def get_all_map_area(db: Session, user_id, body: FilterSchema):
    try:
        data = db.query(MarkMapArea)
        if "type" in body.filter:
            if body.filter['start_date'] == MAP_TYPE.AREA:
                data = data.filter(MarkMapArea.type == MAP_TYPE.AREA)
            else:
                data = data.filter(MarkMapArea.type == MAP_TYPE.MISSION)    
        if "user_id" in body.filter:
            data = data.filter(MarkMapArea.user_id == user_id)        
        if "start_date" in body.filter:
            data = data.filter(MarkMapArea.created_at >= body.filter['start_date'])
        if "end_date" in body.filter:
            data = data.filter(MarkMapArea.created_at <= body.filter['end_date'])
        if "area_id" in body.filter:
            data = data.filter(MarkMapArea.id == body.filter['area_id'])
        if "name" in body.filter:
            data = data.filter(MarkMapArea.name.contains(body.filter['name']))
        if "code" in body.filter:
            data = data.filter(MarkMapArea.code.contains(body.filter['code']))
        if "active" in body.filter:
            data = data.filter(MarkMapArea.active == body.filter['active'])
        # if "user_ids" in body.filter:
        #     data = data.filter(MarkMapArea.user_ids.contains(body.filter['user_ids']))
        total_record = data.count()
        offset = body.page_index * body.page_size
        data = data.order_by(MarkMapArea.created_at.desc()).offset(offset).limit(
            body.page_size).all()
        for i in data:
            if i.properties:
                i.properties = json.loads(i.properties)
            if i.geometry:
                i.geometry = json.loads(i.geometry)
            if i.meta_data:
                i.meta_data = json.loads(i.meta_data)


        return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi hệ thống.")

def get_mark_map_by_id(db: Session, id: int):
    data = db.query(MarkMapArea).filter(MarkMapArea.type == MAP_TYPE.AREA, MarkMapArea.id == id).first()
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Khu vuc không tồn tại")
 
    return ResultResponseSchema(data=data, total_record=1, status=200, message="Thành công")   

def get_mark_map(db: Session, id: int):
    
    data = db.query(MarkMapArea).filter(MarkMapArea.type == MAP_TYPE.AREA, MarkMapArea.id == id).first()
 
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Khu vuc không tồn tại")
    if data:
        if data.properties:
            data.properties = json.loads(data.properties)
        if data.geometry:
            data.geometry = json.loads(data.geometry)
        if data.meta_data:
            data.meta_data = json.loads(data.meta_data)

    return ResultResponseSchema(data=data, total_record=1, status=200, message="Thành công")   

def create_mark_map(db: Session, markmaparea: MarkMapAreaCreateSchema, user_id):
    try:
        db_item = MarkMapArea(
            name=markmaparea.name,
            geometry=json.dumps(markmaparea.geometry),
            properties=json.dumps(markmaparea.properties),
            meta_data=json.dumps(markmaparea.meta_data),
            user_id=user_id,
            type=MAP_TYPE.AREA,
            active=True,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(db_item)
        db.commit()
        # db.close()

        db.refresh(db_item)

        item = db.query(MarkMapArea).get(db_item.id)
        item.code = f'HS{db_item.id}'
        db.commit()

        if item.properties:
            item.properties = json.loads(item.properties)
        if item.geometry:
            item.geometry = json.loads(item.geometry)
        if item.meta_data:
            item.meta_data = json.loads(item.meta_data)

        return item
        
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi hệ thống.")

def update_mark_map(id: int, db: Session, body: MarkMapAreaUpdateSchema, user_id):
    try:
        item = db.query(MarkMapArea).get(id)
        if not item:
            raise HTTPException(
                status_code=404, detail=f"Khu vuc không tồn tại")
       
        item.name = body.name
        item.geometry = json.dumps(body.geometry)
        item.properties = json.dumps(body.properties)
        item.meta_data = json.dumps(body.meta_data)
        item.user_id = user_id
        item.type = MAP_TYPE.AREA
        item.active = True
        item.updated_at = datetime.now()
        db.commit()
        row = db.query(MarkMapArea).get(id)
        
        return row
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi hệ thống.")

def delete_mark_map(id: int, db: Session):
    item = db.query(MarkMapArea).get(id)
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Khu vuc không tồn tại")

def get_mark_map_by_coordinates(db: Session, coordinates: str):
    return db.query(MarkMapArea).filter(MarkMapArea.geometry['coordinates'] == coordinates).first()

def get_current_id(request):
    user_login = decodeJWT(
        request.headers['authorization'].replace('Bearer ', ''))

    return user_login['user_id']

 # todo list mission profile in backend
def get_all_mission_profile(db: Session, user_id, body: FilterSchema):
    data = db.query(MarkMapArea)
    if "type" in body.filter:
        data = data.filter(MarkMapArea.type == body.filter['type'])
    else:
        data = db.query(MarkMapArea).filter(MarkMapArea.type == MAP_TYPE.MISSION)

    data = data.filter(or_(MarkMapArea.user_id == user_id, text(f"user_ids @> '[{user_id}]'")))
    
    if "start_date" in body.filter:
        data = data.filter(MarkMapArea.created_at >= body.filter['start_date'])
    if "end_date" in body.filter:
        data = data.filter(MarkMapArea.created_at <= body.filter['end_date'])
    if "keyword" in body.filter:
        data = data.filter(
            or_(MarkMapArea.name.contains(body.filter['keyword']),
                MarkMapArea.code.contains(body.filter['keyword'])))
    if "active" in body.filter:
        data = data.filter(MarkMapArea.active == body.filter['active'])
    
    total_record = data.count()
    offset = body.page_index * body.page_size
    data = data.order_by(MarkMapArea.created_at.desc()).offset(offset).limit(
        body.page_size).all()
    for i in data:
        user_info = db.query(User).filter(User.id == i.user_id).first()
        if user_info:
            i.user_name = user_info.full_name
            i.user_email = user_info.email
        if i.properties:
            i.properties = json.loads(i.properties)
        if i.geometry:
            i.geometry = json.loads(i.geometry)
        if i.meta_data:
            i.meta_data = json.loads(i.meta_data)
        if i.user_ids:
            list_user_name = []
            for rows in i.user_ids:
                item = db.query(User).filter(User.active == True, User.id == rows).first()
                if item:
                    list_user_name.append(item.full_name)
            i.list_user_name = list_user_name
       
    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")

# todo detail mission profile in backend
def get_mission_profile_by_id(db: Session, id: int):
    data = db.query(MarkMapArea).filter(MarkMapArea.type == MAP_TYPE.MISSION, MarkMapArea.id == id).first()
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Nhiệm vụ không tồn tại")
   
    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")

def get_mission_profile(db: Session, id: int):
    data = db.query(MarkMapArea).filter(MarkMapArea.type == MAP_TYPE.MISSION, MarkMapArea.id == id).first()
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Nhiệm vụ không tồn tại")
    if data:
        user_info = db.query(User).get(data.user_id)
        if user_info:
            data.user_name = user_info.full_name
            data.user_email = user_info.email
        if data.properties:
            data.properties = json.loads(data.properties)
        if data.geometry:
            data.geometry = json.loads(data.geometry)
        if data.meta_data:
            data.meta_data = json.loads(data.meta_data)
        if data.user_ids:
            list_user_name = []
            for rows in data.user_ids:
                item = db.query(User).filter(User.active == True, User.id == rows).first()
                if item:
                    list_user_name.append(item.full_name)
            data.list_user_name = list_user_name

    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")

# todo create mission profile in backend
def create_mission_profile(db: Session, markmaparea: MissionProfileCreateSchema, user_id):   
    db_item = MarkMapArea(
        name=markmaparea.name,
        description=markmaparea.description,
        user_ids=markmaparea.user_ids,
        geometry=json.dumps(markmaparea.geometry),
        properties=json.dumps(markmaparea.properties),
        meta_data=json.dumps(markmaparea.meta_data),
        user_id=user_id,
        type=MAP_TYPE.MISSION,
        active=markmaparea.active,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    db.add(db_item)
    db.commit()
    # db.close()
    db.refresh(db_item)
    item = db.query(MarkMapArea).get(db_item.id)
    item.code = f'NV{db_item.id}'
    db.commit()
    if item.properties:
        item.properties = json.loads(item.properties)
    if item.geometry:
        item.geometry = json.loads(item.geometry)
    if item.meta_data:
        item.meta_data = json.loads(item.meta_data)

    return item

# todo update mission profile in backend
def update_mission_profile(id: int, db: Session, body: MissionProfileUpdateSchema, user_id):
    item = db.query(MarkMapArea).filter(MarkMapArea.type == MAP_TYPE.MISSION, MarkMapArea.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Nhiệm vụ không tồn tại")

    item.name = body.name
    item.description = body.description
    item.user_ids = body.user_ids
    item.geometry = json.dumps(body.geometry)
    item.properties = json.dumps(body.properties)
    item.meta_data = json.dumps(body.meta_data)
    item.user_id = user_id
    item.active = body.active
    item.updated_at = datetime.now()

    db.commit()
    row = db.query(MarkMapArea).filter(MarkMapArea.type == MAP_TYPE.MISSION, MarkMapArea.id == id).first()
  
    return row

# todo delete mission profile in backend
def delete_mission_profile(id: int, db: Session):
    item = db.query(MarkMapArea).filter(MarkMapArea.type == MAP_TYPE.MISSION, MarkMapArea.id == id).first()
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Nhiệm vụ không tồn tại")


def get_filter_mission_profile(db: Session, user_id, body: FilterSchema):
    # polygon_conver = ''
    # if "coordinates" in body.filter:
    #     polygon_conver = system_service.convert_polygon(body.filter['coordinates'])

    # data = db.query(MarkMapArea).from_statement(
    #     sqlalchemy.text(
    #         "SELECT * FROM mark_map_areas where ST_OVERLAPS(mark_map_areas.properties, 'POLYGON ((104.78759765625 20.365227537412434, 106.72119140625 20.365227537412434, 106.72119140625 21.657428197370653, 104.78759765625 21.657428197370653, 104.78759765625 20.365227537412434))') = true")).all()


    return ListResponseSchema(data={}, total_record=1, status=200, message="Thành công")

def export_excel_map_area(db: Session, user_id, body: FilterSchema):
    try:
        data = db.query(MarkMapArea)
        if "type" in body.filter:
            if body.filter['start_date'] == MAP_TYPE.AREA:
                data = data.filter(MarkMapArea.type == MAP_TYPE.AREA)
            else:
                data = data.filter(MarkMapArea.type == MAP_TYPE.MISSION)    
        if "user_id" in body.filter:
            data = data.filter(MarkMapArea.user_id == user_id)        
        if "start_date" in body.filter:
            data = data.filter(MarkMapArea.created_at >= body.filter['start_date'])
        if "end_date" in body.filter:
            data = data.filter(MarkMapArea.created_at <= body.filter['end_date'])
        if "area_id" in body.filter:
            data = data.filter(MarkMapArea.id == body.filter['area_id'])
        if "name" in body.filter:
            data = data.filter(MarkMapArea.name.contains(body.filter['name']))
        if "code" in body.filter:
            data = data.filter(MarkMapArea.code.contains(body.filter['code']))
        if "active" in body.filter:
            data = data.filter(MarkMapArea.active == body.filter['active'])
            
        offset = body.page_index * body.page_size
        data = data.order_by(MarkMapArea.created_at.desc()).offset(offset).limit(
            body.page_size).all()
        for i in data:
            user_info = db.query(User).filter(User.id == i.user_id).first()
            if user_info:
                i.user_name = user_info.full_name
                i.user_email = user_info.email
        #     if i.properties:
        #         i.properties = json.loads(i.properties)
        #     if i.geometry:
        #         i.geometry = json.loads(i.geometry)
        #     if i.meta_data:
        #         i.meta_data = json.loads(i.meta_data)

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail="Lỗi hệ thống.")