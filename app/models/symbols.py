from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from databases.db import Base


class Symbols(Base):
    __tablename__ = 'symbols'

    id = Column(Integer(), primary_key=True, index=True)
    label = Column(String(), default=True)
    v_label = Column(String())
    object_name = Column(Text())
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
