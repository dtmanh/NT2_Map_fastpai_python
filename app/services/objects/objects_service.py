import json
from fastapi import HTTPException
from app.models.object_layers import ObjectLayers
from app.models.objects import Objects
from app.models.symbols import Symbols
from app.schemas.respose_schema import ListResponseSchema
from app.services.objects.schemas.objects_schema import ObjectCreateSchema, ObjectUpdateSchema, ObjectIDSchema
from databases.db import Session
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT

def get_all_by_user_id(db: Session, user_id, params: ObjectIDSchema):

    object_layer_id = params.object_layer_id
    data = db.query(Objects).filter(Objects.user_id == user_id)
    if object_layer_id > 0:
        data = data.filter(Objects.object_layer_id == object_layer_id)

    if "name" in params.filter:
        data = data.filter(Objects.name.contains(params.filter['name']))

    total_record = data.count()
    offset = params.page_index * params.page_size

    data = data.order_by(Objects.created_at.desc()).offset(offset).limit(
        params.page_size).all()

    for i in data:
        symbol = db.query(Symbols).filter(Symbols.id == i.symbol_id).first()
        if i.properties:
            i.properties = json.loads(i.properties)
        else:
            i.properties ={}
        if i.geometry:
            i.geometry = json.loads(i.geometry)
        if symbol:
            i.properties.update({"symbol": symbol.label})

    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")

def create_object(db: Session, user_id: int, object: ObjectCreateSchema):
    db_item = Objects(
        name=object.name,
        description=object.description,
        tags=object.tags,
        object_layer_id=object.object_layer_id,
        user_id=user_id,
        image=json.dumps(object.image),
        properties=json.dumps(object.properties),
        geometry=json.dumps(object.geometry),
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    item = db.query(Objects).get(db_item.id)

    return item

def update_object(id: int, user_id, db: Session, body: ObjectUpdateSchema):
    item = db.query(Objects).filter(Objects.user_id == user_id, Objects.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")

    item.name = body.name
    item.description = body.description
    item.tags = body.tags
    item.image = json.dumps(body.image)
    item.object_layer_id = body.object_layer_id
    item.user_id = user_id
    item.properties = json.dumps(body.properties)
    item.geometry = json.dumps(body.geometry)
    item.updated_at = datetime.now()
    db.commit()
    return db.query(Objects).filter(Objects.user_id == user_id, Objects.id == id).first()

def delete_object(user_id:int, id: int, db: Session):
    item = db.query(Objects).filter(Objects.id == id, Objects.user_id == user_id).first()
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")

def check_object_id(db: Session, user_id, object_id):
    data = db.query(Objects).filter(Objects.user_id == user_id, Objects.id == object_id).first()

    return data
def get_object_by_id(db: Session, id: int):
    data = db.query(Objects).filter(Objects.id == id).first()
    
    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")

def get_object(db: Session, id: int):
    data = db.query(Objects).filter(Objects.id == id).first()
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")
    if data:
        symbol = db.query(Symbols).filter(Symbols.id == data.symbol_id).first()
        if data.properties:
            data.properties = json.loads(data.properties)
        else:
            data.properties = {}
        if data.geometry:
            data.geometry = json.loads(data.geometry)
        if symbol:
            data.properties.update({"symbol": symbol.label})

    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")

