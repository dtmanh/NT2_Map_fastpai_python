from sqlalchemy import Column, Integer, String, Boolean, DateTime

from databases.db import Base

class SystemConfig(Base):
    __tablename__ = 'system_configs'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(),  nullable=False)
    key = Column(String(),  nullable=False)
    key_value = Column(String(),  nullable=False)
    type = Column(String())
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
    deleted_by = Column(String(), default=None)
    deleted_at = Column(DateTime(), default=None)

