# from sqlalchemy import Column, Integer, String, DateTime, Boolean
# from databases.db import Base


# class RobotConfig(Base):
#     __tablename__ = 'robot_configs'

#     id = Column(Integer(), primary_key=True, index=True)
#     key = Column(String(), nullable=False, index=True)
#     key_value = Column(String(), nullable=False)
#     type = Column(String(), nullable=False)
#     created_at = Column(DateTime(), default=None)
#     updated_at = Column(DateTime(), default=None)
#     deleted_by = Column(String(), default=None)
#     deleted_at = Column(DateTime(), default=None)
