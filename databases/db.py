from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker


from config import get_config

# gọi config từ file config, .env
db_host = get_config('DB_HOST')
db_name = get_config('DB_NAME')
db_user = get_config('DB_USER')
db_password = get_config('DB_PASSWORD')
db_post = get_config('DB_PORT')
SQLALCHEMY_DATABASE_URL = f'postgresql://{db_user}:{db_password}@{db_host}:{db_post}/{db_name}'
#SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)

# khởi tạo session
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.bind = engine


def get_db():
    """
    Generator function for dependency injection to fetch a new session on a new request
    """
    db = Session()
    try:
        yield db
    finally:
        db.close()

