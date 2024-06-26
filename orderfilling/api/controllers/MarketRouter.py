from fastapi import APIRouter
from orderfilling.api.controllers import (
    MarketDataRestController,
    MarketOrderRestController,
)

router = APIRouter(prefix="/api")

router.include_router(MarketDataRestController.router)
router.include_router(MarketOrderRestController.router)
