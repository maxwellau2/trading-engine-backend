import asyncio
import json
from fastapi import FastAPI, Request, Response
from orderfilling.api.controllers import (
    MarketDataRestController,
    WSController,
    sample_connection_controller,
    MarketRouter,
)
from orderfilling.api.utils.OrderBookMonitor import monitor_order_book
from users.controller import UsersController
from users.login.controller import Login
from fastapi.middleware.cors import CORSMiddleware
from middleware.UserAuth import UserAuth

app = FastAPI()
app_auth = FastAPI()

origins = [
    "http://localhost",
    "http://127.0.0.1",
    "http://127.0.0.1:5173/",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app_auth.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app_auth.middleware("http")
# async def verifyJWT(request: Request, call_next):
#     if "payload" not in request.headers:
#         response = json.dumps({"message": "forbidden"})
#         return Response(status_code= 403, content=response)
#     else:
#         token = request.headers.get('payload')
#         is_valid_user = UserAuth.check_jwt(token)
#         if is_valid_user:
#             response = await call_next(request)
#             return response
#         else:
#             res = json.dumps({"message": "invalid jwt"})
#             return Response(status_code=403, content=res)


app.include_router(WSController.router)
app.include_router(UsersController.router)
app.include_router(sample_connection_controller.router)
app.include_router(Login.router)
app.include_router(MarketDataRestController.router)

app_auth.include_router(MarketRouter.router)

app.mount("/trade", app_auth)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_order_book())

@app.on_event("shutdown")
async def shutdown_event():
    # save all data to db
    pass


# fastapi dev main.py
