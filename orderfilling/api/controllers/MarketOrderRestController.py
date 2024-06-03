from fastapi import APIRouter
from orderfilling.orderbook.currency_singleton import currency
from orderfilling.orderbook.OrderbookPool import OrderBookPool
from pydantic import BaseModel

pool = OrderBookPool()
router = APIRouter(prefix="/trading", tags=["Trading Endpoints"])

class Item(BaseModel):
    ticker: str
    qty: float

class Order(BaseModel):
    ticker: str
    side: str
    qty: float
    price: float


@router.post("/fill_order")
async def fill_order(item:Item):
    book = pool.get_order_book_by_name(item.ticker)
    if not book:
        return {"message": "invalid ticker"}
    book.__currency_manager__.fill_order(item.qty)
    # currency.fill_order(coins)
    return {"message": "Order filled", "state": book.get_market_state().__dict__}

@router.post("/place_order")
async def place_order(order:Order):
    book = pool.get_order_book_by_name(order.ticker)
    if not book:
        return {"message": "invalid ticker"}
    if order.side.upper() == "BUY":
        order = book.add_bid_order(size=order.qty, price=order.price)
        return order
    elif order.side.upper() == "SELL":
        order = book.add_ask_order(size=order.qty, price=order.price)
        return order
    return None
