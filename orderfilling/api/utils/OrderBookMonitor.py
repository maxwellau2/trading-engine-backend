import asyncio
from orderfilling.orderbook.OrderbookPool import OrderBookPool

orderbooks = [
    {"name": "coin1", "total_market_value": 100, "available_liquidity": 5},
    {"name": "coin2", "total_market_value": 100, "available_liquidity": 10},
    {"name": "coin3", "total_market_value": 100, "available_liquidity": 1000},
]


async def monitor_order_book():
    order_book_pool = OrderBookPool()
    for i in orderbooks:
        order_book_pool.create_order_book(
            i["name"],
            i["total_market_value"],
            available_liquidity=i["available_liquidity"],
        )
    # order_book = order_book_pool.get_order_book_by_name(order_book_name)
    while True:
        orderbook_dict = order_book_pool.get_order_books()
        for i in orderbook_dict:
            orderbook_dict[i].fill_available_orders()
        # order_book.fill_available_orders()
        await asyncio.sleep(0.5)  # Adjust the interval as needed

