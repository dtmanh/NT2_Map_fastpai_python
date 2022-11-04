import time
import jwt
# from jose import JWTError, jwt
from config import get_config

from app.services.auth.schemas.auth_schema import UserLoginReponseSchema, UserLoginWithTokenReponseSchema

JWT_SECRET = get_config('secret')
JWT_ALGORITHM = get_config('algorithm')

def signJWT(user):

    payload = {
        "user_id": user.id,
        "expires": time.time() + 60000,
        "role_id": user.role_id,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    
    return UserLoginWithTokenReponseSchema(
        access_token=token,
        data=UserLoginReponseSchema(email=user.email, phone=user.phone)
    )

def decodeJWT(token: str):
    try:
        decode_token = jwt.decode(token, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >= time.time() else None
    except:
        return {}

# def auth_logout(payload):
#     print('test payload 1', payload)
#     payload['expires'] = 0
#     print('test payload', payload)
#     token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
#     return True
    
# def refresh_token(data: dict, expires_delta: Union[timedelta, None] = None):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
#     return encoded_jwt