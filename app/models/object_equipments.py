from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from databases.db import Base


class ObjectEquipments(Base):
    __tablename__ = 'object_equipments'

    id = Column(Integer(), primary_key=True, index=True)
    description = Column(String(255), unique=True, default=True)
    attributes = Column(JSON(), nullable=True)
    equipment_id = Column(Integer(), ForeignKey("equipments.id", ondelete="CASCADE"), index=True)
    object_id = Column(Integer(), ForeignKey("objects.id", ondelete="CASCADE"), index=True)
    quantity = Column(Integer(), nullable=True)
    radius = Column(Float(), nullable=True)
    created_at = Column(DateTime(), default=None, nullable=True)
    updated_at = Column(DateTime(), default=None, nullable=True)
