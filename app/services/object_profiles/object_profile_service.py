import json
from fastapi import HTTPException
from app.models.object_profile import ObjectProfile
from app.schemas.respose_schema import ListResponseSchema
from app.services.object_profiles.schemas.object_profile_schema import ObjectProfileCreateSchema, ObjectProfileUpdateSchema
from databases.db import Session
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT

def get_all_by_user_id(db: Session, id, user_id):
    data = db.query(ObjectProfile).filter(ObjectProfile.user_id == user_id, ObjectProfile.id == id)
    total_record = data.count()
    data = data.all()
    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")


def create_object_profile(db: Session, user_id: int, object_profile: ObjectProfileCreateSchema):
    db_item = ObjectProfile(
        user_id=user_id,
        name=object_profile.name,
        description=object_profile.description,
        content=object_profile.content,
        geometry=json.dumps(object_profile.geometry),
        properties=json.dumps(object_profile.properties),
        type=object_profile.type,
        created_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    # db.close()
    db.refresh(db_item)
    item = db.query(ObjectProfile).get(db_item.id)
    return item

def update_object_profile(id: int, user_id, db: Session, body: ObjectProfileUpdateSchema):
    item = db.query(ObjectProfile).get(id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Hồ sơ không tồn tại")

    item.name = body.name
    item.description = body.description
    item.content = body.content
    item.user_id = user_id
    item.type = body.type
    item.geometry = json.dumps(body.geometry)
    item.properties = json.dumps(body.properties)
    item.updated_at = datetime.now()
    db.commit()
    return db.query(ObjectProfile).get(id)

def delete_object_profile(user_id:int, id: int, db: Session):
    item = db.query(ObjectProfile).filter(ObjectProfile.id == id, ObjectProfile.user_id == user_id).first()
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Hồ sơ không tồn tại")