from fastapi import APIRouter
from orderfilling.orderbook.currency_singleton import currency
from orderfilling.orderbook.OrderbookPool import OrderBookPool
from pydantic import BaseModel


pool = OrderBookPool()
router = APIRouter(prefix="/market_data", tags=["Market Data Endpoints"])

@router.get("/users")
async def read_users():
    return [{"name" : "Jonathan Tan"}, {"name": "poopooman"}]

@router.get("/market_value")
async def get_market_value(ticker: str):
    book = pool.get_order_book_by_name(ticker)
    if not book:
        return {"message": "ticker not found"}
    market_state = book.get_market_state()
    return market_state.__dict__

@router.get("/open_orders")
async def get_open_orders(ticker:str):
    book = pool.get_order_book_by_name(ticker)
    if not book:
        return {"message": "ticker not found"}
    return book.get_all_orders()