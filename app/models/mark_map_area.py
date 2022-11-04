from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Float, Text
from sqlalchemy.dialects.postgresql import JSONB
from geoalchemy2 import Geometry
from sqlalchemy.orm import relationship
from databases.db import Base


class MarkMapArea(Base):
    __tablename__ = 'mark_map_areas'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String())
    description = Column(Text())
    type = Column(String())
    code = Column(Text())
    geometry = Column(Text(), default=None)
    properties = Column(Text(), default=None)
    meta_data = Column(Text(), default=None)
    active = Column(Boolean(), default=None)
    user_id = Column(Integer())
    user_ids = Column(JSONB())
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)


