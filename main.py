import asyncio
from fastapi import FastAPI
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

app = FastAPI()

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
# origins = ["*"]

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(WSController.router)
# app.include_router(MarketDataRestController.router)
app.include_router(MarketRouter.router)
app.include_router(UsersController.router)
app.include_router(sample_connection_controller.router)
app.include_router(Login.router)


@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_order_book())


# fastapi dev main.py
