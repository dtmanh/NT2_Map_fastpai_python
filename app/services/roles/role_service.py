from functools import cache
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import and_
from sqlalchemy.orm import load_only
from app.models.role import Role
from app.models.user import User
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.services.roles.schemas.RoleCreateSchema import RoleCreateSchema
from app.services.roles_permissions import role_permission_service
from databases.db import Session
from app.schemas import respose_schema

def getAllRoles(db: Session, name_role):
    try:
        data = db.query(Role)
        if name_role:
            data = data.filter(Role.name.contains(name_role))
        data = data.all()

        return data
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

def get_role(db: Session, role_id: int):
    try:
        data = db.query(Role).filter(Role.id == role_id).first()
        if data.id:
            data_permission = db.query(RolePermission).join(Permission).with_entities(RolePermission.permission_id, Permission.module.label("permission_module"), Permission.name.label("permission_name"), Permission.key.label("permission_key")).filter(RolePermission.role_id == data.id).all()
            data.__dict__["action"] = data_permission

        return respose_schema.ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")
    except Exception as err:
        if isinstance(err, HTTPException):
            raise err
        raise HTTPException(status_code=500, detail=str(err))    

def createNewRole(db: Session, body: RoleCreateSchema):
    try:
        db_role = Role(name=body.role_name, is_system=body.is_system, created_at=datetime.now())
        db.add(db_role)
        db.commit()
        # db.close()
        db.refresh(db_role)

        role_id = db_role.id
        list_action = body.permission.split(',')
        if role_id:
            list_action_old = role_permission_service.get_role_permission_by_role(db, role_id)
        if list_action_old:
            Check_Update_Role_permission(db, role_id, list_action, list_action_old)
        item = db.query(Role).get(role_id)
        return respose_schema.ResultResponseSchema(data=item, status=200, message="Thêm mới thành công")
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"Vui lòng kiểm tra lại dữ liệu")

def update_role(id: int, db: Session, body: RoleCreateSchema):
    item = db.query(Role).get(id)

    if not item:
        raise HTTPException(
            status_code=404, detail=f"Role không tồn tại")
    try:
        item.name = body.role_name
        item.is_system = body.is_system
        item.updated_at = datetime.now()
        db.commit()

        list_action = body.permission.split(',')
        list_action_old = role_permission_service.get_role_permission_by_role(db, id)
        if list_action_old:
            Check_Update_Role_permission(db, id, list_action, list_action_old)
        data = db.query(Role).get(id)

        return respose_schema.ResultResponseSchema(data=data, status=200, message="Cập nhật thành công")
    except Exception:
        raise HTTPException(
            status_code=404, detail=f"Vui lòng kiểm tra lại dữ liệu")

def Check_Update_Role_permission(db, role_id, list_action, list_action_old):
    # if todo check item in list. if no exists then delete item
    for ac_old in list_action_old:
        if str(ac_old.permission_id) not in list_action:
            role_permission_service.delete_role_permission(db, role_id, ac_old.permission_id)
    # if todo if item exists in list  then insert role permission
    for ac in list_action:
        check = role_permission_service.get_role_permission(db, role_id, ac)
        if not check:
            role_permission_service.create_role_permission(db, role_id, ac)

    return True

def delete_role(id: int, db: Session):
    # if todo item check role in user
    check = db.query(User).filter(User.role_id == id).first()
    if check:
        raise HTTPException(
            status_code=404, detail=f"Đã có thành viên được phân quyền nhóm role này")

    item = db.query(Role).get(id)
    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        # if todo delete tavle role_permission it from the database.
        list_RolePermission = db.query(RolePermission).filter(RolePermission.role_id == id).all()
        for rol in list_RolePermission:
            role_permission_service.delete_role_permission_by_id(db, rol.id)
        try:
            db.delete(item)
            db.commit()
            db.close()
        except Exception:
            raise HTTPException(
                status_code=404, detail=f"Vui lòng kiểm tra lại dữ liệu")
    else:
        raise HTTPException(
            status_code=404, detail=f"Role không tồn tại")
