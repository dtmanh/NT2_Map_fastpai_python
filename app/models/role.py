from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from databases.db import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer(), primary_key=True, nullable=False)
    name = Column(String(255), nullable=False)
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
    deleted_by = Column(String(), default=None)
    deleted_at = Column(DateTime(), default=None)
    is_system = Column(Boolean(), default=False)

    items = relationship("RolePermission", back_populates="owner_role")
    owner = relationship("User", back_populates="items_role")