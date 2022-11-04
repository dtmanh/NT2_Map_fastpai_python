from app.schemas.filter_schema import FilterSchema
from app.services.source_data_collection.schemas.source_data_collections_schema import SourceDataCollectionCreateSchema, SourceDataCollectionUpdateSchema
from fastapi import HTTPException
from app.models.source_data_collection import SourceDataCollection
from app.schemas.respose_schema import ListResponseSchema
from databases.db import Session
from datetime import datetime

# region Lấy danh sách nguồn thu thập dữ liệu
def list(db: Session, user_id: int, params: FilterSchema):
    data = db.query(SourceDataCollection).filter(SourceDataCollection.user_id == user_id, SourceDataCollection.is_available == False)
    if "name" in params.filter:
        data = data.filter(SourceDataCollection.name.contains(params.filter['name']))

    # data = db.query(Objects).filter(Objects.user_id == user_id)   
    total_record = data.count()
    offset = params.page_index * params.page_size
    data = data.order_by(SourceDataCollection.created_at.desc()).offset(offset).limit(
        params.page_size).all()
    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")
# endregion

# region Lấy danh sách nguồn thu thập dữ liệu is_available = True
def list_available(db: Session, params: FilterSchema):
    data = db.query(SourceDataCollection).filter(SourceDataCollection.is_available == True)
    # data = db.query(Objects).filter(Objects.user_id == user_id)
    total_record = data.count()
    # offset = params.page_index * params.page_size
    data = data.order_by(SourceDataCollection.created_at.desc()).all()
    return ListResponseSchema(data=data, total_record=total_record, status=200, message="Thành công")
# endregion

# region Lấy thông tin nguồn thu thập dữ liệu
def get_detail(db: Session, id: int):
    data = db.query(SourceDataCollection).filter(SourceDataCollection.id == id).first()

    if not data:
        return ListResponseSchema(data={}, total_record=1, status=404, message="Nguồn thu thập dữ liệu không tồn tại")

    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")
# endregion

# region Tạo thông tin nguồn thu thập dữ liệu
def create(db: Session, user_id: int, body: SourceDataCollectionCreateSchema):
    db_item = SourceDataCollection(
        name=body.name,
        description=body.description,
        url=body.url,
        priority=body.priority,
        is_available=body.is_available,
        user_id=user_id,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    item = db.query(SourceDataCollection).get(db_item.id)

    return item
# endregion

# region Tạo thông tin nguồn thu thập dữ liệu
def update(id: int, user_id, db: Session, body: SourceDataCollectionUpdateSchema):
    item = db.query(SourceDataCollection).filter(SourceDataCollection.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Nguồn dữ liệu không tồn tại")
    item.name=body.name
    item.description=body.description
    item.url=body.url
    item.priority=body.priority
    item.is_available=body.is_available
    item.updated_at=datetime.now()
    db.commit()
    return db.query(SourceDataCollection).filter(SourceDataCollection.user_id == user_id, SourceDataCollection.id == id).first()
# endregion

# region Xóa nguồn thu thập dữ liệu
def delete(id: int, db: Session):
    item = db.query(SourceDataCollection).filter(SourceDataCollection.id == id).first()
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Nguồn dữ liệu không tồn tại")
# endregion