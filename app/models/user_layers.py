from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from databases.db import Base


class UserLayer(Base):
    __tablename__ = 'user_layers'

    id = Column(Integer(), primary_key=True, index=True)
    layer_id = Column(Text(), unique=True, default=True)
    user_id = Column(Integer(), ForeignKey("users.id"), index=True)
    tags = Column(Text())
    geometry = Column(Text(), default=None)
    properties = Column(Text(), default=None)
    meta_data = Column(Text(), default=None)
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
