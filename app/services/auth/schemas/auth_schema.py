from pydantic import BaseModel, Field, EmailStr

class UserLoginSchema(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)
    class Config:
        orm_mode = True
        
class UserLoginReponseSchema(BaseModel):
    email: EmailStr = Field(...)
    phone: str = Field(...)
    class Config:
        orm_mode = True
        
class UserLoginWithTokenReponseSchema(BaseModel):
    access_token: str
    data: UserLoginReponseSchema
    class Config:
        orm_mode = True
