from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Float, Text

from sqlalchemy.orm import relationship
from databases.db import Base


class SourceDataCollection(Base):
    __tablename__ = 'source_data_collections'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String())
    description = Column(String())
    url = Column(String())
    priority = Column(Integer(), default=None)
    is_available = Column(Boolean(), default=False)
    user_id = Column(Integer(), default=None)
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)


