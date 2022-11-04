from fastapi import HTTPException
from passlib.context import CryptContext
from app.models.user import User
from app.models.role import Role
from app.services.auth.auth_handle import signJWT
from app.services.auth.schemas.auth_schema import UserLoginSchema
from datetime import datetime

from databases.db import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(db: Session, body: UserLoginSchema, is_system):
    time_now = datetime.now()
    user = db.query(User).filter(User.email == body.email).first()
    if not user:
        raise HTTPException(
            status_code=404, detail="Tài khoản không tồn tại")    
    if user:
        if user.expired_time < time_now:
            raise HTTPException(
                status_code=422, detail="Tài khoản của bạn hết hạn đăng nhập")
        if not verify_password(body.password, user.password):
            raise HTTPException(
                status_code=422, detail="Mật khẩu không đúng")

        if user.active == False:
            raise HTTPException(
                status_code=401, detail="Tài khoản chưa được active")
        if user.role_id:        
            role = db.query(Role).filter(Role.id == user.role_id).first()
            if not role:
                raise HTTPException(
                    status_code=404, detail="Tài khoản Chưa được phân quyền")
            if role.is_system != is_system:
                raise HTTPException(
                    status_code=401, detail="Tài khoản không được phép đăng nhập")

    return signJWT(user)
