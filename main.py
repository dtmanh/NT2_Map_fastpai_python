import uvicorn
from fastapi import FastAPI, Request

from app.controllers import register_routes
from app.services.auth.auth_handle import decodeJWT
from databases.db import SQLALCHEMY_DATABASE_URL
# from app.services.middleware.middleware import Check_role
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI(debug=True)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# def catch_exceptions_middleware(request: Request, call_next):
#     # if(request & request.headers):
#     # print('request main: ', request.headers['authorization'].replace('Bearer ', ''))
#     # print('decode token main: ', decodeJWT(request.headers['authorization'].replace('Bearer ', '')))
#     if(request.headers['authorization']):
#         user = decodeJWT(request.headers['authorization'].replace('Bearer ', ''))
#     return call_next(request)
#
# app.middleware('http')(catch_exceptions_middleware)

# app.middleware('http')(Check_role)


register_routes(app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)
