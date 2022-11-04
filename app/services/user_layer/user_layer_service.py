import json
from fastapi import HTTPException
from app.models.user_layers import UserLayer
from app.schemas.respose_schema import ListResponseSchema
from app.services.user_layer.schemas.user_layer_schema import UserLayerUpdateSchema, UserLayerCreateSchema, UserLayerIDSchema
from databases.db import Session
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT

def get_all_by_user_id(db: Session, user_id, params: UserLayerIDSchema):

    layer_id = params.layer_id
    data = db.query(UserLayer).filter(UserLayer.user_id == user_id)
    if layer_id:
        data = data.filter(UserLayer.layer_id == layer_id)
    total_record = 0
    if layer_id:
        data = data.first()
        if data:
            total_record = 1
            data.geometry = json.loads(data.geometry)
            data.properties = json.loads(data.properties)
            data.meta_data = json.loads(data.meta_data)
    else:
        total_record = data.count()
        data = data.all()
        for i in data:
            i.geometry = json.loads(i.geometry)
            i.properties = json.loads(i.properties)
            i.meta_data = json.loads(i.meta_data)
    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")

def create_user_layer(db: Session, user_id: int, user_layer: UserLayerCreateSchema):
    db_item = UserLayer(
        tags=user_layer.tags,
        layer_id=user_layer.layer_id,
        user_id=user_id,
        geometry=json.dumps(user_layer.geometry),
        properties=json.dumps(user_layer.properties),
        meta_data=json.dumps(user_layer.meta_data),
        created_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    # db.close()
    db.refresh(db_item)
    item = db.query(UserLayer).get(db_item.id)

    return item

def update_user_layer(id: int, user_id, db: Session, body: UserLayerUpdateSchema):
    item = db.query(UserLayer).filter(UserLayer.user_id == user_id, UserLayer.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Layer không tồn tại")

    item.tags = body.tags
    item.user_id = user_id
    item.geometry = json.dumps(body.geometry)
    item.properties = json.dumps(body.properties)
    item.meta_data = json.dumps(body.meta_data)
    item.updated_at = datetime.now()
    db.commit()
    return db.query(UserLayer).filter(UserLayer.user_id == user_id, UserLayer.id == id).first()

def delete_user_layer(user_id:int, id: int, db: Session):
    item = db.query(UserLayer).filter(UserLayer.id == id, UserLayer.user_id == user_id).first()
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Layer không tồn tại")

def check_user_layer_id(db: Session, user_id, layer_id):
    data = db.query(UserLayer).filter(UserLayer.user_id == user_id, UserLayer.layer_id == layer_id).first()

    return data