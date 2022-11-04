import json
from fastapi import HTTPException
from passlib.context import CryptContext
from app.models.user import User
from app.models.history_search import HistorySearch
from app.models.fillter_search import FillterSearch
from app.services.satellite.satellite_handle import TokenVendor
from app.services.auth.schemas.auth_schema import UserLoginSchema
from app.services.satellite.schemas.HistorySearch_schema import HistorySearchCreateSchema
from app.services.satellite.schemas.fillter_search_schema import FillterSearchCreateSchema
from app.schemas import respose_schema
from datetime import datetime
from databases.db import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db: Session, body: UserLoginSchema):

    return TokenVendor()

def get_data(db: Session, user_id: int, page_size, page_index):
    offset = page_index * page_size
    data = db.query(HistorySearch).filter(HistorySearch.user_id == user_id).offset(offset).limit(
        page_size).all()
    return data

def CreateNewHistorySearch(user_id, db: Session, body: HistorySearchCreateSchema):
    db_HistorySearch = HistorySearch(user_id=user_id, data_search=json.dumps(body.data_search))
    db.add(db_HistorySearch)
    db.commit()
    # db.close()
    db.refresh(db_HistorySearch)
    item = db.query(HistorySearch).get(db_HistorySearch.id)

    return respose_schema.ResultResponseSchema(data=item, status=200, message="Thêm mới thành công")

def GetFillterSearch_by_user_id(user_id, db: Session):
    return db.query(FillterSearch).filter(FillterSearch.user_id == user_id).first()

def CreateNewFillterSearch(user_id, db: Session, body: FillterSearchCreateSchema):
    db_FillterSearch = FillterSearch(user_id=user_id, data_fillter=json.dumps(body.data_fillter), created_at=datetime.now(), updated_at=datetime.now())
    db.add(db_FillterSearch)
    db.commit()
    # db.close()
    db.refresh(db_HistorySearch)
    item = db.query(FillterSearch).get(db_FillterSearch.id)

    return respose_schema.ResultResponseSchema(data=item, status=200, message="Thêm mới thành công")

def UpdateFillterSearch(id: int, db: Session, body: FillterSearchCreateSchema):
    item = db.query(FillterSearch).get(id)
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Fillter search không tồn tại")

    item.data_fillter = json.dumps(body.data_fillter)
    item.updated_at = datetime.now()
    db.commit()
    return db.query(FillterSearch).get(id)
