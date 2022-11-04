from sqlalchemy import Column, Integer, ForeignKey, Text

from sqlalchemy.orm import relationship
from databases.db import Base


class HistorySearch(Base):
    __tablename__ = 'history_searchs'

    id = Column(Integer(), primary_key=True, index=True)
    user_id = Column(Integer(), nullable=False)
    data_search = Column(Text(), unique=True, nullable=False, default=[])
