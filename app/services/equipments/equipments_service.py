import json
from fastapi import HTTPException
from app.models.equipments import Equipments
from app.schemas.respose_schema import ListResponseSchema
from app.services.equipments.schemas.equipments_schema import EquipmentCreateSchema, EquipmentIDSchema, EquipmentUpdateSchema
from databases.db import Session
from sqlalchemy.orm import load_only
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT
from app.models.object_equipments import ObjectEquipments

def get_all_equipments(db: Session, params: EquipmentIDSchema):

    data = db.query(Equipments)
    if "name" in params.filter:
        data = data.filter(Equipments.name.contains(params.filter['name']))

    if "code" in params.filter:
        data = data.filter(Equipments.code.contains(params.filter['code']))

    total_record = data.count()
    offset = params.page_index * params.page_size

    data = data.order_by(Equipments.created_at.desc()).offset(offset).limit(
        params.page_size).all()

    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")

def create_equipment(db: Session, object: EquipmentCreateSchema):
    db_item = Equipments(
        name=object.name,
        code=object.code,
        radius=object.radius,
        description=object.description,
        attributes=object.attributes,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    item = db.query(Equipments).get(db_item.id)

    return item

def update_equipments(id: int, db: Session, body: EquipmentUpdateSchema):
    item = db.query(Equipments).get(id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Trang thiết bị không tồn tại")
    try:
        item.name = body.name
        item.code = body.code
        item.radius = body.radius
        item.description = body.description
        item.attributes = body.attributes
        item.updated_at = datetime.now()
        db.commit()
        db.refresh(item)

        return ListResponseSchema(data=db.query(Equipments).get(id), total_record=1, status=200, message="Cập nhật thành công")
    except Exception as e:
            raise HTTPException(status_code=500, detail="Lỗi hệ thống.")
            
def delete_equipments(id: int, db: Session):
    item = db.query(Equipments).get(id)
    if item:
        try:
            db.delete(item)
            db.commit()
            db.close()
        except Exception as e:
            raise HTTPException(status_code=500, detail="Lỗi hệ thống.")
    else:
        raise HTTPException(
            status_code=404, detail=f"Trang thiết bị không tồn tại")

    return item

def get_detail(db: Session, id: int):
    data = db.query(Equipments).get(id)
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Trang thiết bị không tồn tại")
   
    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")