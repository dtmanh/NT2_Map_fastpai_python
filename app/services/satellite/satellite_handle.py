import jwt
import time
import requests
from datetime import datetime, timedelta
from config import get_config

def TokenVendor():
    secret_key = get_config('SECRET_VKEY_VENDOR')
    now = datetime.now()
    exp_time = now + timedelta(seconds=120)
    header_auth = {
        "typ": "JWT",
        "alg": get_config('algorithm'),
        "iss": get_config('ISS'),
        "exp": exp_time.timestamp()
    }
    encoded_jwt = jwt.encode(header_auth, secret_key, algorithm="HS256")
    token = encoded_jwt.decode('utf-8')

    return token