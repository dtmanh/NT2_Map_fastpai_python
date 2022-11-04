
from operator import index
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from databases.db import Base

    
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer(), primary_key=True, index=True)
    role_id = Column(Integer(), ForeignKey("roles.id"), nullable=False)
    full_name = Column(String(255))
    first_name = Column(String(100))
    last_name = Column(String(100))
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(12), unique=True)
    password = Column(String(), nullable=False)
    partner_unit = Column(String(), nullable=True)
    note = Column(String(), nullable=True)
    is_online = Column(Boolean(), default=False)
    active = Column(Boolean(), default=True)
    created_by = Column(String())
    expired_time = Column(DateTime(), nullable=True)
    created_at = Column(DateTime(), nullable=True)

    items_log = relationship("SystemLog", back_populates="owner")
    # items_config = relationship("UserConfig", back_populates="owner")
    items_role = relationship("Role", back_populates="owner")
