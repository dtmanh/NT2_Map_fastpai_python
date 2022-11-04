from fastapi import HTTPException
from app.models.area_profile import AreaProfile
from app.schemas.respose_schema import ListResponseSchema
from app.services.area_profile.schemas.area_profile_schema import AreaProfileCreateSchema, AreaProfileUpdateSchema
from databases.db import Session
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT

def get_all_by_user_id(db: Session, area_id, user_id):
    data = db.query(AreaProfile).filter(AreaProfile.area_id == area_id, AreaProfile.user_id == user_id)
    total_record = data.count()
    data = data.all()
    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")


def create_area_profile(db: Session, user_id: int, area_profile: AreaProfileCreateSchema):
    db_item = AreaProfile(
        area_id=area_profile.area_id,
        user_id=user_id,
        name=area_profile.name,
        type=area_profile.type,
        lever=area_profile.lever,
        content=area_profile.content,
        created_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    # db.close()
    db.refresh(db_item)
    item = db.query(AreaProfile).get(db_item.id)

    return item

def update_area_profile(id: int, db: Session, body: AreaProfileUpdateSchema):
    item = db.query(AreaProfile).get(id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Hồ sơ không tồn tại")

    item.name = body.name
    item.area_id = body.area_id
    item.user_id = body.user_id
    item.type = body.type
    item.lever = body.lever
    item.content = body.content
    item.updated_at = datetime.now()
    db.commit()
    # db.refresh(db_item)
    return db.query(AreaProfile).get(id)

def delete_area_profile(user_id:int, id: int, db: Session):
    item = db.query(AreaProfile).filter(AreaProfile.id == id, AreaProfile.user_id == user_id).first()
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Hồ sơ không tồn tại")