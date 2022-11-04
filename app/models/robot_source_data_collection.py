from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Float, Text

from sqlalchemy.orm import relationship
from databases.db import Base


class RobotSourceDataCollection(Base):
    __tablename__ = 'config_robot_source_data_collections'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String(), default=None)
    description = Column(String(), default=None)
    source_id = Column(String(), default=None)
    priority = Column(Integer(), default=None)
    frequency = Column(String(), default=None)
    type_data = Column(String(), default=None)
    status = Column(String(), default=None)
    attribute = Column(JSON, default=None)
    geometry = Column(JSON, default=None)
    is_check = Column(Boolean(), default=False)
    start_time = Column(DateTime(), default=None)
    end_time = Column(DateTime(), default=None)
    user_id = Column(Integer(), ForeignKey("users.id"), index=True, default=None)
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)


