from fastapi import APIRouter, HTTPException
from orderfilling.orderbook.OrderbookPool import OrderBookPool
from pydantic import BaseModel
from fastapi.responses import JSONResponse


pool = OrderBookPool()
router = APIRouter(prefix="/market_data", tags=["Market Data Endpoints"])

@router.get("/market_state")
async def get_market_state(ticker: str):
    book = pool.get_order_book_by_name(ticker)
    if not book:
        raise HTTPException(status_code=404, detail= {"message": "ticker not found"})
    price = book.get_vwap_price()
    spread = book.get_bid_ask_spread()
    mid_price = book.get_mid_price()
    return {"price": price, "spread": spread, "mid_price": mid_price}

@router.get("/open_orders")
async def get_open_orders(ticker:str):
    book = pool.get_order_book_by_name(ticker)
    if not book:
        return {"message": "ticker not found"}
    return book.get_all_orders() 
