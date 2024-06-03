import asyncio
from fastapi import FastAPI
from orderfilling.api.controllers import MarketDataRestController, WSController, sample_connection_controller, MarketRouter
from orderfilling.api.utils.OrderBookMonitor import monitor_order_book

app = FastAPI()

# orderbooks = [
#     {
#         "name" : "coin1",
#         "total_market_value" : 100,
#         "available_liquidity" : 5
#     },
#     {
#         "name" : "coin2",
#         "total_market_value" : 100,
#         "available_liquidity" : 10
#     },
#     {
#         "name" : "coin1",
#         "total_market_value" : 100,
#         "available_liquidity" : 1000
#     },
# ]

app.include_router(WSController.router)
# app.include_router(MarketDataRestController.router)
app.include_router(MarketRouter.router)
app.include_router(sample_connection_controller.router)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(monitor_order_book())
# fastapi dev main.py