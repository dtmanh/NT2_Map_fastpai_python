from app.models import system_config, user, user_config, system_log, permission, role_permission, role, robot_config

from .db import engine

def init_db():
    user.Base.metadata.create_all(bind=engine)
    user_config.Base.metadata.create_all(bind=engine)
    system_config.Base.metadata.create_all(bind=engine)
    system_log.Base.metadata.create_all(bind=engine)
    permission.Base.metadata.create_all(bind=engine)
    role_permission.Base.metadata.create_all(bind=engine)
    role.Base.metadata.create_all(bind=engine)
    robot_config.Base.metadata.create_all(bind=engine)
