from fastapi import FastAPI
from orderfilling.controllers import marketdata_controller, marketdata_ws_controller, sample_connection_controller

app = FastAPI()

app.include_router(marketdata_ws_controller.router)
app.include_router(marketdata_controller.router)
app.include_router(sample_connection_controller.router)

# fastapi dev main.py