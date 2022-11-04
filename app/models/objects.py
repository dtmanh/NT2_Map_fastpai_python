from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from databases.db import Base


class Objects(Base):
    __tablename__ = 'objects'

    id = Column(Integer(), primary_key=True, index=True)
    object_layer_id = Column(Integer(), default=True)
    user_id = Column(Integer(), ForeignKey("users.id"), index=True)
    name = Column(Text())
    description = Column(Text())
    tags = Column(Text())
    symbol_id = Column(Integer())
    image = Column(Text())
    properties = Column(Text(), default=None)
    geometry = Column(Text(), default=None)
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
