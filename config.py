import os

from dotenv import load_dotenv

load_dotenv()

# gọi config từ file .env
def get_config(key):
    return os.getenv(key)
