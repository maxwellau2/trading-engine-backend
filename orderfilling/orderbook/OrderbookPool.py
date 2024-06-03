from typing import Dict
from orderfilling.orderbook.Orderbook import OrderBook

class OrderBookPool:
    _instance = None
    _order_books = {}

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def create_order_book(self, name:str, total_market_value:float, available_liquidity:float) -> OrderBook:
        if name not in self._order_books:
            self._order_books[name] = OrderBook(name, total_market_value, available_liquidity)
        return self._order_books[name]
    
    def get_order_book_by_name(self, name:str) -> OrderBook:
        """
        returns Orderbook if ticker in orderbook
        returns None is ticker not found
        """
        if name not in self._order_books:
            return None
        return self._order_books[name]

    def get_order_books(self) -> Dict[str,OrderBook]:
        return self._order_books