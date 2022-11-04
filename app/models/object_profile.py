from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, Float, Text

from sqlalchemy.orm import relationship
from databases.db import Base


class ObjectProfile(Base):
    __tablename__ = 'object_profiles'

    id = Column(Integer(), primary_key=True, index=True)
    name = Column(String())
    description = Column(String())
    content = Column(Text(), default=None)
    geometry = Column(Text(), default=None)
    properties = Column(Text(), default=None)
    type = Column(String(), default=None)
    user_id = Column(Integer())
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)


