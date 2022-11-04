from sqlalchemy import Column, Integer, ForeignKey, Text, DateTime

from sqlalchemy.orm import relationship
from databases.db import Base


class FillterSearch(Base):
    __tablename__ = 'user_fillter_configs'

    id = Column(Integer(), primary_key=True, index=True)
    user_id = Column(Integer(), nullable=False)
    data_fillter = Column(Text(), unique=True, nullable=False, default=[])
    created_at = Column(DateTime(), default=None)
    updated_at = Column(DateTime(), default=None)
