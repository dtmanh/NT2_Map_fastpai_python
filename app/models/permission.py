from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from databases.db import Base


class Permission(Base):
    __tablename__ = 'permissions'

    id = Column(Integer(), primary_key=True, nullable=False, index=True)
    name = Column(String(255), nullable=False)
    key = Column(String(255), nullable=False)
    module = Column(String(255), nullable=False)
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
    deleted_by = Column(String(), default=None)
    deleted_at = Column(DateTime(), default=None)

    items = relationship("RolePermission", back_populates="owner_permission")
