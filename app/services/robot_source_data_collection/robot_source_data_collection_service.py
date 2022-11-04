from app.models.robot_source_data_collection import RobotSourceDataCollection
from app.schemas.filter_schema import FilterSchema
from app.services.robot_source_data_collection.schemas.robot_source_data_collections_schema import ListRobotSourceDataCollectionSchema, RobotSourceDataCollectionCreateSchema, RobotSourceDataCollectionUpdateSchema
# from app.services.robot_source_data_collections_schema.schemas.robot_source_data_collections_schema import RobotSourceDataCollectionCreateSchema, RobotSourceDataCollectionUpdateSchema
from fastapi import HTTPException
from app.schemas.respose_schema import ListResponseSchema
from databases.db import Session

# region Lấy danh sách nguồn thu thập dữ liệu
def list(db: Session, params: FilterSchema):
    data = db.query(RobotSourceDataCollection)
    total_record = data.count()
    offset = params.page_index * params.page_size
    data = data.order_by(RobotSourceDataCollection.created_at.desc()).offset(offset).limit(
        params.page_size).all()
    return ListRobotSourceDataCollectionSchema(data=data, total_record=total_record, status=200, message="Thành công")
# endregion

# region Lấy thông tin nguồn thu thập dữ liệu
def get_detail(db: Session, id: int):
    data = db.query(RobotSourceDataCollection).filter(RobotSourceDataCollection.id == id).first()

    if not data:
        return ListResponseSchema(data={}, total_record=1, status=404, message="Nguồn thu thập dữ liệu không tồn tại")

    return ListResponseSchema(data=data, total_record=1, status=200, message="Thành công")
# endregion

# region Tạo thông tin nguồn thu thập dữ liệu
def create(db: Session, user_id: int, body: RobotSourceDataCollectionCreateSchema):
    db_item = RobotSourceDataCollection(
        name=body.name,
        description=body.description,
        source_id=body.source_id,
        priority=body.priority,
        frequency=body.frequency,
        attribute=body.attribute,
        is_check=body.is_check,
        start_time=body.start_time,
        end_time=body.end_time,
        user_id=user_id,
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    
    item = db.query(RobotSourceDataCollection).get(db_item.id)

    return item
# endregion

# region Tạo thông tin nguồn thu thập dữ liệu
def update(id: int, user_id, db: Session, body: RobotSourceDataCollectionUpdateSchema):
    item = db.query(RobotSourceDataCollection).filter(RobotSourceDataCollection.id == id).first()
    if not item:
        raise HTTPException(
            status_code=404, detail=f"Nguồn dữ liệu không tồn tại")
    item.name=body.name
    item.description=body.description
    item.source_id=body.source_id
    item.priority=body.priority
    item.frequency=body.frequency
    item.attribute=body.attribute
    item.is_check=body.is_check
    item.start_time=body.start_time
    item.end_time=body.end_time
    item.user_id=user_id
    db.commit()
    return db.query(RobotSourceDataCollection).filter(RobotSourceDataCollection.user_id == user_id, RobotSourceDataCollection.id == id).first()
# endregion

# region Xóa nguồn thu thập dữ liệu
def delete(id: int, db: Session):
    item = db.query(RobotSourceDataCollection).filter(RobotSourceDataCollection.id == id).first()
    if item:
        db.delete(item)
        db.commit()
        db.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"Nguồn dữ liệu không tồn tại")
# endregion