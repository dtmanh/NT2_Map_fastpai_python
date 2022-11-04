import json
from fastapi import HTTPException
from pydantic import ValidationError
from app.models.object_layers import ObjectLayers
from app.models.objects import Objects
from app.models.symbols import Symbols
from app.schemas.filter_schema import FilterSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.object_layers.schemas.object_layers_schema import ObjectLayersCreateSchema, ObjectLayersUpdateSchema
from databases.db import Session
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT
from app.services.system import system_service

def get_all_by_user_id(db: Session, user_id):
    data = db.query(ObjectLayers).filter(ObjectLayers.user_id == user_id)
    total_record = data.count()
    data = data.all()
    for i in data:
        object = db.query(Objects).filter(Objects.user_id == user_id, Objects.object_layer_id == i.id).all()
        if object:
            for j in object:
                j.image = json.loads(j.image) if bool(j.image) else {}
                j.properties = json.loads(j.properties) if bool(j.properties) else {}
                j.geometry = json.loads(j.geometry) if bool(j.properties) else {"type": "Polygon","coordinates": []}
                if j.symbol_id:
                    symbol = db.query(Symbols).filter(Symbols.id == j.symbol_id).first()
                    j.properties = j.properties.update({"symbol": symbol.label}) if symbol.label else j.properties

            i.features = object

    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")

def create_object_layer(db: Session, user_id: int, object_layer: ObjectLayersCreateSchema):

    db_item = ObjectLayers(
        name=object_layer.name,
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    # db.close()
    db.refresh(db_item)
    item = db.query(ObjectLayers).get(db_item.id)
    return item

def update_object_layer(id: int, user_id, db: Session, body: ObjectLayersUpdateSchema):
    item = db.query(ObjectLayers).filter(ObjectLayers.user_id == user_id, ObjectLayers.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Lớp không tồn tại")

    item.name = body.name
    item.updated_at = datetime.now()
    db.commit()
    return db.query(ObjectLayers).filter(ObjectLayers.user_id == user_id, ObjectLayers.id == id).first()

def delete_object_layer(user_id:int, id: int, db: Session):
    item = db.query(ObjectLayers).filter(ObjectLayers.id == id, ObjectLayers.user_id == user_id).first()
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Lớp không tồn tại")

def get_object_layer_by_id(db: Session, id: int):
    data = db.query(ObjectLayers).filter(ObjectLayers.id == id).first()
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Lớp không tồn tại")
    
    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")

def get_object_layer(db: Session, id: int):
    data = db.query(ObjectLayers).filter(ObjectLayers.id == id).first()
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Lớp không tồn tại")
    if data:
        object = db.query(Objects).filter(Objects.object_layer_id == id).all()
        if object:
            for j in object:
                j.image = json.loads(j.image) if bool(j.image) else {}
                j.properties = json.loads(j.properties) if bool(j.properties) else {}
                j.geometry = json.loads(j.geometry) if bool(j.geometry) else {"type": "Polygon", "coordinates": []}
                if j.symbol_id:
                    symbol = db.query(Symbols).filter(Symbols.id == j.symbol_id).first()
                    j.properties = j.properties.update({"symbol": symbol.label}) if symbol.label else j.properties
            data.features = object

    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")

def get_all_symbols(db: Session):
    data = db.query(Symbols).all()
    return data

def create_object_by_file_csv(db: Session, user_id, id: int, data):
    data_item = db.query(ObjectLayers).filter(ObjectLayers.user_id == user_id, ObjectLayers.id == id).first()
    if not data_item:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")

    kq = data['WKT'].split()

    properties = {"color": "#0288d1", "symbol": "marker"}
    geometry = {}
    coordinates = []
    if kq[0] == "POINT":
        geometry["type"] = 'Point'
        geometry["coordinates"] = [float(data['Lon']),float(data['Lat'])]
        system_service.Check_point(float(data['Lon']), float(data['Lat']))

    else:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")

        char_to_replace = {'POLYGON ': '', '(': '', ')': ''}
        geometry["type"] = 'Polygon'
        for key, value in char_to_replace.items():
            data['WKT'] = data['WKT'].replace(key, value)

        for rows in data['WKT'].split(','):
            point = rows.split()
            system_service.Check_point(float(point[0]), float(point[0]))
            coordinates.append([float(point[0]),float(point[1])])

        geometry["coordinates"] = [coordinates]

    db_item = Objects(
        name=data['name'],
        description=data['description'] if bool(data['description']) else '',
        object_layer_id=id,
        user_id=user_id,
        properties=json.dumps(properties),
        geometry=json.dumps(geometry),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    db.close()

    return True

def create_object_by_file_xlsx(db: Session, user_id, id: int, data):
    data_item = db.query(ObjectLayers).filter(ObjectLayers.user_id == user_id, ObjectLayers.id == id).first()
    if not data_item:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")
    geometry = {}
    coordinates = []
    properties = {"color": "#0288d1", "symbol": "marker"}
    check = False
    if data['WKT'] == "POINT":
        geometry["type"] = 'Point'
        check = True
        geometry["coordinates"] = [float(data['Lon']),float(data['Lat'])]
        system_service.Check_point(float(data['Lon']), float(data['Lat']))

    if data['WKT'] == "POLYGON":
        char_to_replace = {'(': '', ')': ''}
        if data['Polygon']:
            geometry["type"] = 'Polygon'
            for key, value in char_to_replace.items():
                data['Polygon'] = data['Polygon'].replace(key, value)

            for rows in data['Polygon'].split(','):
                point = rows.split()
                system_service.Check_point(float(point[0]), float(point[1]))
                coordinates.append([float(point[0]),float(point[1])])

            geometry["coordinates"] = [coordinates]
            check = True

    if check:
        db_item = Objects(
            name=data['name'],
            description=data['description'],
            object_layer_id=id,
            user_id=user_id,
            properties=json.dumps(properties),
            geometry=json.dumps(geometry),
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        db.add(db_item)
        db.commit()
        db.close()

    return True

def create_object_by_file_json(db: Session, user_id, id: int, data):
    data_item = db.query(Objects).filter(Objects.user_id == user_id, Objects.id == id).first()
    if not data_item:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")

    if data['type'] == "Point":
        system_service.Check_point(float(data['coordinates'][0]), float(data['coordinates'][1]))

    if data['type'] == "POLYGON":
        for row in data['coordinates'][0]:
            system_service.Check_point(float(row[0]), float(row[1]))

    properties = {"color": "#0288d1", "symbol": "marker"}
    db_item = Objects(
        name='vi tri',
        description='',
        object_layer_id=id,
        user_id=user_id,
        properties=json.dumps(properties),
        geometry=json.dumps(data),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    db.close()

    return True
