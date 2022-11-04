import json
from fastapi import HTTPException
from app.models.object_equipments import ObjectEquipments
from app.models.objects import Objects
# from app.models.symbols import Symbols
from app.schemas.respose_schema import ListResponseSchema
from app.services.object_equipments.schemas.object_equipments_schema import ObjectEquipmentUpdateSchema, ObjectEquipmentCreateSchema, ObjectEquipmentIDSchema
from databases.db import Session
from datetime import datetime
from app.services.auth.auth_handle import decodeJWT
from app.models.equipments import Equipments

def get_all_equiqments(db: Session, object_id):
    item = db.query(Objects).get(object_id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")
            
    data = db.query(ObjectEquipments).join(Equipments).with_entities(Equipments.name,ObjectEquipments.id,ObjectEquipments.description,ObjectEquipments.attributes,ObjectEquipments.equipment_id,ObjectEquipments.object_id,ObjectEquipments.quantity,ObjectEquipments.radius,ObjectEquipments.created_at,ObjectEquipments.updated_at).filter(ObjectEquipments.object_id == object_id)    
    total_record = data.count()
    data = data.order_by(ObjectEquipments.created_at.desc()).all()

    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")

def get_all_equipments_left(db: Session, object_id):
    item = db.query(Objects).get(object_id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Đối tượng không tồn tại")
    # danh sach thiet bi da chon
    list_equipment = db.query(ObjectEquipments.equipment_id).filter(ObjectEquipments.object_id == object_id).all()    
    list = [obj.equipment_id for obj in list_equipment]
    #  danh sach thiet bi chưa chon
    data = db.query(Equipments).filter(~Equipments.id.in_(list))
    total_record = data.count()
    data = data.all()

    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")    

def create_object_equipment(db: Session, object: ObjectEquipmentCreateSchema):
    db_item = ObjectEquipments(
        description=object.description,
        radius=object.radius,
        quantity=object.quantity,
        attributes=object.attributes,
        equipment_id=object.equipment_id,
        object_id=object.object_id,
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    item = db.query(ObjectEquipments).get(db_item.id)

    return item

def update_object_equipment(id: int, db: Session, body: ObjectEquipmentUpdateSchema):
    item = db.query(ObjectEquipments).get(id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Trang thiết bị không tồn tại")

    item.description = body.description
    item.radius = body.radius
    item.quantity = body.quantity
    item.attributes = body.attributes
    item.updated_at = datetime.now()
    db.commit()
    db.refresh(item)

    return ListResponseSchema(data=db.query(ObjectEquipments).get(id), total_record=1, status=200, message="Thành công")
  

def delete_object_equipments(id: int, db: Session):
    item = db.query(ObjectEquipments).get(id)
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Trang thiết bị không tồn tại")

    return True

def get_detail(db: Session, id: int):
    data = db.query(ObjectEquipments).join(Equipments).with_entities(Equipments.name,ObjectEquipments.description,ObjectEquipments.attributes,ObjectEquipments.equipment_id,ObjectEquipments.object_id,ObjectEquipments.quantity,ObjectEquipments.radius,ObjectEquipments.created_at,ObjectEquipments.updated_at).filter(ObjectEquipments.id == id).first()
    if not data:
        raise HTTPException(
            status_code=404, detail=f"Trang thiết bị không tồn tại")
   
    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")

