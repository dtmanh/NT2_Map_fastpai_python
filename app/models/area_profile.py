from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from databases.db import Base


class AreaProfile(Base):
    __tablename__ = 'area_profiles'

    id = Column(Integer(), primary_key=True, index=True)
    area_id = Column(Integer(), ForeignKey("mark_map_areas.id"), index=True)
    user_id = Column(Integer(), ForeignKey("users.id"), index=True)
    name = Column(String(), default=None)
    type = Column(String(), default=None)
    lever = Column(Integer(), default=None)
    content = Column(Text(), default=None)
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
    deleted_by = Column(String(), default=None)
    deleted_at = Column(DateTime(), default=None)
