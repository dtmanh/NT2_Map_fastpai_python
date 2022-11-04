from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text, JSON, FLOAT
from sqlalchemy.orm import relationship
from databases.db import Base


class Equipments(Base):
    __tablename__ = 'equipments'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(255), nullable=True)
    code = Column(String(30), default=None, nullable=True)
    attributes = Column(JSON(), nullable=True)
    description = Column(Text(), nullable=True)
    radius = Column(FLOAT(), nullable=True)
    created_at = Column(DateTime(), default=None, nullable=True)
    updated_at = Column(DateTime(), default=None, nullable=True)
