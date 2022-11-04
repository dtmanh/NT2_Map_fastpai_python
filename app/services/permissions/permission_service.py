from datetime import datetime
from sqlalchemy import and_
from app.models.permission import Permission
from app.services.permissions.schemas.PermissionSchema import PermissionCreateSchema
from databases.db import Session
from fastapi import HTTPException
from app.schemas import respose_schema


def getAllRolePermission(db: Session):
    list = db.query(Permission).all()

    return respose_schema.ResultResponseSchema(data=list, status=200, message="Danh sach quyền")

def createNewPermission(db: Session, body: PermissionCreateSchema):
    try:
        db_permission = Permission(name=body.permission_name, key=body.key, module=body.module, created_at=datetime.now(), updated_at=datetime.now())
        db.add(db_permission)
        db.commit()
        # db.close()
        db.refresh(db_permission)
        item = db.query(Permission).get(db_permission.id)

        return respose_schema.ResultResponseSchema(data=item, status=200, message="Thêm thành công")
    except HTTPException:
        raise HTTPException(
            status_code=404, detail=f"Error!. Vui long kiểm tra lại dữ liệu")

def update_permission(id: int, db: Session, body: PermissionCreateSchema):
    item = db.query(Permission).get(id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Permission không tồn tại")

    item.name = body.permission_name
    item.key = body.key
    item.module = body.module
    item.updated_at=datetime.now()
    db.commit()
    return db.query(Permission).get(id)

def delete_permission(id: int, db: Session):

    item = db.query(Permission).get(id)
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Permission không tồn tại")
