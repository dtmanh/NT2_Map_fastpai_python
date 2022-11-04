from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Text
from sqlalchemy.orm import relationship
from databases.db import Base


class SystemLog(Base):
    __tablename__ = 'system_logs'

    id = Column(BigInteger(), primary_key=True, nullable=False, index=True)
    user_id = Column(Integer(), ForeignKey("users.id"), nullable=False)
    action = Column(String())
    type = Column(String())
    method = Column(String())
    url = Column(String())
    ip = Column(String())
    user_agent = Column(String())
    accept = Column(String())
    description = Column(Text())
    warehouse = Column(Text())
    created_at = Column(DateTime(), default=datetime.now())
    detail = Column(Text(), nullable=False)

    owner = relationship("User", back_populates="items_log")
