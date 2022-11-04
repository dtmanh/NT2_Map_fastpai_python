from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from databases.db import Base


class RolePermission(Base):
    __tablename__ = 'role_permission'

    id = Column(Integer(), primary_key=True, nullable=False)
    role_id = Column(Integer(), ForeignKey("roles.id"), nullable=False)
    permission_id = Column(Integer(), ForeignKey("permissions.id"), nullable=False)

    owner_role = relationship("Role", back_populates="items")
    owner_permission = relationship("Permission", back_populates="items")

