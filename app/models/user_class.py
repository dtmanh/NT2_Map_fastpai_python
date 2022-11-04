from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from databases.db import Base


class UserClass(Base):
    __tablename__ = 'user_class'

    id = Column(Integer(), primary_key=True, index=True)
    layer_id = Column(Text(), unique=True, default=True)
    name = Column(Text(), default=None)
    data = Column(Text(), default=None)
    user_id = Column(Integer(), ForeignKey("users.id"), index=True)
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
