from array import array
from fastapi import HTTPException
from app.schemas.respose_schema import ListResponseSchema, ResultResponseSchema
from sqlalchemy.orm import load_only
from app.services.mark_map_area.schemas.mark_map_area_schema import MarkMapAreaCreateSchema, MarkMapAreaUpdateSchema
from databases.db import Session
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT
from app.models.user import User


def get_current_id(request):
    user_login = decodeJWT(
        request.headers['authorization'].replace('Bearer ', ''))

    return user_login['user_id']

def get_current_email(db: Session, request):
    user_login = decodeJWT(
        request.headers['authorization'].replace('Bearer ', ''))
    user = db.query(User).options(load_only(*["email"])).filter(User.id == user_login['user_id']).first()

    return user.email


def is_valid_geometry_json(obj):
    title = 'type'
    if "coordinates" not in obj or title not in obj or obj['type'] not in ["Point", "Polygon"] or obj['coordinates'] == []:
        raise HTTPException(status_code=422, detail=f"Please check file and geometry")

    if obj['type'] == "Point":
        if len(obj['coordinates']) != 2:
            raise HTTPException(status_code=422, detail='the "coordinates" member must be a single position')

    if obj['type'] == "Polygon":
        coord = obj['coordinates']
        lengths = all([len(elem) >= 4 for elem in coord])
        if lengths is False:
            raise HTTPException(status_code=422, detail='LinearRing must contain with 4 or more positions')

        # isring = all([elem[0] == elem[-1] for elem in coord])
        # if isring is False:
        #     raise HTTPException(status_code=422, detail='The first and last positions in LinearRing must be equivalent')

    return True

def convert_polygon(polygon):
    content = ''
    for row in polygon:
        for item in row:
            content += str(item[0]) +' '+str(item[1])+ ','

    mang = 'POLYGON(('+ content[:-1] +'))'
    return mang

def Check_point(lng, lat):
    if lng <= -180.0 or lng >= 180.0:
        raise HTTPException(status_code=422, detail='Vui lòng kiểm tra lại tọa độ lng')
    if lat <= -90.0 or lat >= 90.0:
        raise HTTPException(status_code=422, detail='Vui lòng kiểm tra lại tọa độ lat')

    return True

def get_field_table(db: Session, table, fields = None, where = None, first: bool=True, offset: int = 0, limit: int = 10):
    
    raise HTTPException(status_code=422, detail=f'{where.User.role_id}')

    data = db.query(table)
    if fields:
       data = data.options(load_only(*fields))

    if where['role_id']:
        data = data.filter(table.role_id == where['role_id'])

    # if where['user_id']:
    #     data = data.filter(table.user_id == where['user_id'])

    total_record = data.count()
   
    if first:
        total_record = 1
        data = data.first()
    else:
        offset = offset * limit
        data = data.order_by(table.id.desc()).offset(offset).limit(limit).all()

    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")

def get_field_table_by_id(db: Session, table, fields = None, id = None, response = True):
    try:
        data = db.query(table)
        if fields:
            data = data.options(load_only(*fields))

        if id:
            data = data.filter(table.id == id)

        data = data.first()

        if response:
            return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")
        else:
            return data

    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))

# delete record in table
def delete_table(db: Session, table, id: int):
    item = db.query(table).get(id)
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        try:
            db.delete(item)
            db.commit()
            db.close()
            return ResultResponseSchema(data=[], status=200, message="Xóa thành công")
        except Exception:
            raise HTTPException(
                status_code=422, detail=f"Error!. Vui lòng kiểm tra lại dữ liệu")       
    else:
        raise HTTPException(
            status_code=404, detail=f"Bản ghi không tồn tại")