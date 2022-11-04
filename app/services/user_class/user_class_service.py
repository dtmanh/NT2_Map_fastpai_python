import json
from fastapi import HTTPException
from pydantic import ValidationError
from app.models.user_class import UserClass
from app.schemas.filter_schema import FilterSchema
from app.schemas.respose_schema import ListResponseSchema
from app.services.user_class.schemas.user_class_schema import UserClassCreateSchema, UserClassUpdateSchema, UserClassIDSchema
from databases.db import Session
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT


def get_all_by_user_id(db: Session, user_id):
    data = db.query(UserClass).filter(UserClass.user_id == user_id)
    total_record = data.count()
    data = data.all()
    for i in data:
        if i.data:
            i.data = json.loads(i.data)
    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")

def create_user_class(db: Session, user_id: int, user_class: UserClassCreateSchema):
    item = db.query(UserClass).filter(UserClass.user_id == user_id, UserClass.layer_id == user_class.layer_id).first()
    if item:
        raise HTTPException(
            status_code=404, detail=f"Lớp đã tồn tại")

    db_item = UserClass(
        name=user_class.name,
        layer_id=user_class.layer_id,
        user_id=user_id,
        data=json.dumps(user_class.data),
        created_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    # db.close()
    db.refresh(db_item)
    item = db.query(UserClass).get(db_item.id)

    return item

def update_user_class(id: int, user_id, db: Session, body: UserClassUpdateSchema):
    item = db.query(UserClass).filter(UserClass.user_id == user_id, UserClass.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Lớp không tồn tại")

    item.name = body.name
    item.data = json.dumps(body.data)
    item.updated_at = datetime.now()
    db.commit()
    return db.query(UserClass).filter(UserClass.user_id == user_id, UserClass.id == id).first()

def delete_user_class(user_id:int, id: int, db: Session):
    item = db.query(UserClass).filter(UserClass.id == id, UserClass.user_id == user_id).first()
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Lớp không tồn tại")
