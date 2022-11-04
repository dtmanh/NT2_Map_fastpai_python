# from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
# from sqlalchemy.orm import relationship
# from databases.db import Base


# class UserConfig(Base):
#     __tablename__ = 'user_configs'

#     id = Column(Integer(), primary_key=True, index=True)
#     user_id = Column(Integer(), ForeignKey("users.id"), index=True)
#     config_content = Column(String())
#     status = Column(Boolean(), default=True)
#     created_at = Column(DateTime(), default=None)
#     updated_at = Column(DateTime(), default=None)
#     deleted_by = Column(String(), default=None)
#     deleted_at = Column(DateTime(), default=None)

#     owner = relationship("User", back_populates="items_config")