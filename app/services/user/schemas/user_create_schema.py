from typing import Union
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreateSchema(BaseModel):
    full_name: str = "admin"
    first_name: str = "super"
    last_name: str = "admin"
    email: EmailStr = 'admin@gmail.com'
    partner_unit: str = 'AHT'
    note: str = 'AHT'
    phone: str = '12312321'
    password: str = 'admin123'
    role_id: int = 1
    is_online: bool = False
    active: bool = True
    created_by = "admin@gmail.com"
    created_at: datetime = datetime.now()
    expired_time: datetime = datetime.now()
    created_at: datetime = datetime.now()

    class Config:
        orm_mode = True


class UserUpdateSchema(BaseModel):
    full_name: str = "admin"
    first_name: str = "super"
    last_name: str = "admin"
    partner_unit: str = 'AHT'
    note: str = 'AHT'
    email: EmailStr = 'admin@gmail.com'
    phone: str = '12312321'
    role_id: int = 1
    active: bool = True
    expired_time: datetime = datetime.now()

    class Config:
        orm_mode = True

class UserResetPasswordSchema(BaseModel):
    password: str = ""
    new_password: str = "123456"

    class Config:
        orm_mode = True