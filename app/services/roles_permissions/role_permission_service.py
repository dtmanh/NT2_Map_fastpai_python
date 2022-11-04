from datetime import datetime
from sqlalchemy import and_
from app.models.role_permission import RolePermission
from app.services.roles_permissions.shemas.roles_permission_schema import RolePermissionCreateSchema
from databases.db import Session
from app.models.permission import Permission

def get_action_role_permission(db: Session, role_id: int):
    data = db.query(RolePermission).join(Permission).with_entities(RolePermission.permission_id, Permission.module.label("permission_module"), Permission.name.label("permission_name"), Permission.key.label("permission_key")).filter(RolePermission.role_id == role_id).all()
    return data

def get_role_permission_by_role(db: Session, role_id: int):
    data = db.query(RolePermission).filter(RolePermission.role_id == role_id).all()
    return data

def get_role_permission(db: Session, role_id: int, permission_id: int):
    data = db.query(RolePermission).filter(RolePermission.role_id == role_id, RolePermission.permission_id == permission_id).first()
    return data

def delete_role_permission(db: Session, role_id: int, permission_id: int):
    item = db.query(RolePermission).filter(RolePermission.role_id == role_id, RolePermission.permission_id == permission_id).first()
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        # db.close()
    return True

def delete_role_permission_by_id(db: Session, id: int):

    item = db.query(RolePermission).get(id)
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        db.delete(item)
        db.commit()
        # db.close()
        return True
    else:
        raise HTTPException(
            status_code=404, detail=f"Role permission not exists")


def create_role_permission(db: Session, role_id: int, permission_id: int):
    try:
        db_data = RolePermission(
            role_id=role_id,
            permission_id=permission_id
        )
        db.add(db_data)
        db.commit()
        db.close()
        return db_data
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"Vui lòng kiểm tra lại dữ liệu")
    