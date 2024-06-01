import asyncio
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from controllers import marketdata_controller, marketdata_ws_controller, sample_connection_controller

app = FastAPI()

app.include_router(marketdata_ws_controller.router)
app.include_router(marketdata_controller.router)
app.include_router(sample_connection_controller.router)