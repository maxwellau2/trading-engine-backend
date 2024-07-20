from fastapi import APIRouter, Response
from orderfilling.orderbook.OrderbookPool import OrderBookPool
from pydantic import BaseModel
import json


pool = OrderBookPool()
router = APIRouter(prefix="/market_data", tags=["Market Data Endpoints"])


@router.get("/market_state")
async def get_market_state(ticker: str):
    book = pool.get_order_book_by_name(ticker)
    if not book:
        return Response(status_code=404, content={"message": "ticker not found"})
    price = book.get_vwap_price()
    spread = book.get_bid_ask_spread()
    mid_price = book.get_mid_price()
    return {"price": price, "spread": spread, "mid_price": mid_price}


@router.get("/open_orders")
async def get_open_orders(ticker: str):
    book = pool.get_order_book_by_name(ticker)
    if not book:
        return Response(status_code=404, content={"message": "ticker not found"})
    response = json.dumps({"message": "success","data":book.get_all_orders()})
    return Response(status_code=200, content=response)

@router.get("/ohlcv")
async def get_ohlcv(ticker: str):
    book = pool.get_order_book_by_name(ticker)
    if not book:
        return Response(status_code=404, content={"message": "ticker not found"})
    response = json.dumps({"message": "success","data":book.get_ohlcv_data()})
    return Response(status_code=200, content=response)

@router.get("/tradehistory")
async def get_ohlcv(ticker: str):
    book = pool.get_order_book_by_name(ticker)
    if not book:
        return Response(status_code=404, content={"message": "ticker not found"})
    response = json.dumps({"message": "success","data":book.get_trade_history()})
    return Response(status_code=200, content=response)
