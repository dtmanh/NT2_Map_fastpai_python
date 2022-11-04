from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import or_
from app.models.role import Role
from app.schemas.filter_schema import FilterSchema
from app.schemas.respose_schema import ListResponseSchema, ResultResponseSchema
from app.services.user.schemas.user_create_schema import UserCreateSchema, UserUpdateSchema, UserResetPasswordSchema
from databases.db import Session
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import load_only
from app.models.user import User
from passlib.context import CryptContext
from app.services.auth.auth_service import verify_password, get_password_hash
from app.services.auth.auth_handle import decodeJWT

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_all(db: Session, body: FilterSchema):

    data = db.query(User).join(Role).with_entities(User.id, User.full_name, User.first_name,
                                                   User.last_name, User.email, User.phone, User.role_id, User.active, User.is_online, Role.name.label("role_name"))

    if "keyword" in body.filter:
        data = data.filter(
            or_(User.full_name.contains(body.filter['keyword']),
                User.email.contains(body.filter['keyword']),
                User.phone.contains(body.filter['keyword'])))

    if "active" in body.filter:
        if(body.filter['active'] == 1):
            body.filter['active'] = True
        else:
            body.filter['active'] = False
        data = data.filter(User.active == body.filter['active'])

    if "role_id" in body.filter:
        data = data.filter(User.role_id == body.filter['role_id'])

    total_record = data.count()

    offset = body.page_index * body.page_size
    data = data.order_by(User.created_at.desc()).offset(offset).limit(
        body.page_size).all()


    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")


def get_user(db: Session, user_id: int):
    data = db.query(User).options(load_only(*["full_name", "first_name", "last_name", "email",
                                              "phone", "role_id", "active", "is_online", "expired_time"])).filter(User.id == user_id).first()

    return ResultResponseSchema(data=data, status=200, message="Thành công")

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_phone(db: Session, phone: str):
    return db.query(User).filter(User.phone == phone).first()


def get_user_by_fullname(db: Session, fullname=Optional[str], record='all'):
    if record == 'all':
        user_detail = db.query(User).filter(
            User.full_name.contains(fullname)).all()
    else:
        user_detail = db.query(User).filter(
            User.full_name.contains(fullname)).first()
    return user_detail


def getError(position, attribute, msg):
    return {
        "loc": [position, attribute],
        "msg": msg,
        "type": f"value.error.{attribute}"
    }


def create_user(db: Session, user: UserCreateSchema):

    isEmailDuplicated = get_user_by_email(db, user.email)

    if(isEmailDuplicated):
        raise HTTPException(
            status_code=422, detail=getError(
                "body", "email", "Email đã tồn tại"))

    isPhoneDuplicated = get_user_by_phone(db, user.phone)
    if(isPhoneDuplicated):
        raise HTTPException(
            status_code=422, detail=getError(
                "body", "phone", "Số điện thoại đã tồn tại"))
    try:
        db_user = User(
            full_name=user.full_name,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone=user.phone,
            password=pwd_context.hash(user.password),
            role_id=user.role_id,
            partner_unit=user.partner_unit,
            note=user.note,
            is_online=user.is_online,
            active=user.active,
            created_by="admin@gmail.com",
            created_at=datetime.now(),
            expired_time=user.expired_time,
        )
        db.add(db_user)
        db.commit()
        # db.close()
        db.refresh(db_user)
        item2 = db.query(User).get(db_user.id)

        return ResultResponseSchema(data=item2, status=200, message="Thêm mới thành công")

    except Exception:
        raise HTTPException(
            status_code=422, detail=f"Error!. Vui lòng kiểm tra lại dữ liệu")    
    

def update_user(id: int, db: Session, body: UserUpdateSchema):

    item = db.query(User).get(id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"User không tồn tại")

    isEmailDuplicated = db.query(User).filter(
        User.email == body.email, User.id != id).first()
    if(isEmailDuplicated):
        raise HTTPException(
            status_code=422, detail=getError(
                "body", "email", "Email đã tồn tại"))

    isPhoneDuplicated = db.query(User).filter(
        User.phone == body.phone, User.id != id).first()
    if(isPhoneDuplicated):
        raise HTTPException(
            status_code=422, detail=getError(
                "body", "phone", "Số điện thoại đã tồn tại"))
    try:
        item.full_name = body.full_name
        item.first_name = body.first_name
        item.last_name = body.last_name
        item.email = body.email
        item.phone = body.phone
        item.partner_unit=body.partner_unit
        item.note=body.note
        item.active = body.active
        item.role_id = body.role_id
        item.expired_time = body.expired_time
        item.updated_at=datetime.now()
        db.commit()
        item =  db.query(User).get(id)
        
        return ResultResponseSchema(data=item, status=200, message="Cập nhật thành công")

    except Exception:
        raise HTTPException(
            status_code=422, detail=f"Error!. Vui lòng kiểm tra lại dữ liệu")    

def delete_user(id: int, db: Session):

    item = db.query(User).get(id)

    # if todo item with given id exists, delete it from the database. Otherwise raise 404 error
    if item:
        try:
            db.delete(item)
            db.commit()
            db.close()
            return ResultResponseSchema(data=[], status=200, message="Xóa thành công")
        except Exception:
            raise HTTPException(
                status_code=422, detail=f"Error!. Vui lòng kiểm tra lại dữ liệu")       
    else:
        raise HTTPException(
            status_code=404, detail=f"User không tồn tại")

def reset_password(db: Session, id, body: UserResetPasswordSchema):
    item = db.query(User).get(id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"User không tồn tại")
            
    # if not verify_password(body.password, item.password):
    #     raise HTTPException(
    #         status_code=422, detail="Mật khẩu cũ không đúng")

    if len(body.new_password) < 6:
        raise HTTPException(
            status_code=422, detail=f"Mật khẩu ít nhất 6 ký tự. Vui lòng kiểm tra lại")

    try:
        item.password = pwd_context.hash(body.new_password)
        item.updated_at=datetime.now(),
        db.commit()
        db.refresh(item)
        item =  db.query(User).get(id)
        return ResultResponseSchema(data=item, status=200, message="Cập nhật thành công")

    except Exception:
        raise HTTPException(
            status_code=422, detail=f"Error!. Vui lòng kiểm tra lại dữ liệu")   

# region  get detail log system
def detail_log(db: Session, request, body):
    user_login = decodeJWT(
            request.headers['authorization'].replace('Bearer ', ''))
    user = db.query(User).options(load_only(*["email"])).filter(User.id == user_login['user_id']).first()
    detail = f"User: {user.email} xem danh sách thành viên" 
    if "keyword" in body.filter:
        detail += f" Từ khóa: {body.filter['keyword']},"
    if "active" in body.filter:
        detail += f" Trạng thái: {body.filter['active']},"
    if "role_id" in body.filter:
        detail += f" Nhóm quyền: {body.filter['role_id']},"
    if "keyword" in body.filter or "active" in body.filter or "role_id" in body.filter:
        detail = detail[:-1]
    return detail
                