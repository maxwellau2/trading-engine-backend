# we will use class composition to define the orderbook
# it is composed of the Currency class as defined in Currency.py
from typing import List
from orderfilling.orderbook.Currency import Currency
from orderfilling.orderbook.PriorityQueue import PriorityQueue
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, OrderWrapper, Side
from orderfilling.orderbook.dataclasses.CurrencyState import CurrencyState
import numpy as np
import time

class OrderBook:
    def __init__(self, name:str, total_market_value:float, available_liquidity:float) -> None:
        self.name = name
        self.__currency_manager__ = Currency(total_market_value=total_market_value, available_liquidity=available_liquidity)
        self.__all_orders__ = PriorityQueue()

    def get_market_state(self) -> CurrencyState:
        return self.__currency_manager__.get_state()
    
    def get_bids(self) -> List[Order]:
        return [wrapper.order for wrapper in self.__all_orders__.sorted_orders if wrapper.order.side == Side.BUY]
    
    def get_asks(self) -> List[Order]:
        return [wrapper.order for wrapper in self.__all_orders__.sorted_orders if wrapper.order.side == Side.SELL]
    

    def get_all_orders(self) -> List[OrderWrapper]:
        """
        returns a sorted list of Orders, including bids and asks
        """
        return self.__all_orders__.sorted_orders
    
    def __check_order_params__(self, size:float, price:float, timenow: int|None) -> bool:
        assert (size > 0), "size has to be a positive integer"
        assert (price > 0), "side has to be a positive integer"
        assert (price > 0), "side has to be a positive integer"
        assert (timenow == None or timenow > 0), "time has to be None or positive"
        return True
    
    def add_bid_order(self, size: float, price: float, timenow: int = None) -> bool:
        """
        size : float > 0
        price: float > 0
        timenow: integer > 0 | None, if none it is generated using epoch time
        assertions will be used
        """
        if self.__check_order_params__(size, price, timenow):
            if not timenow:
                timenow = int(time.time())
            new_order = Order(time=timenow, side=Side.BUY, order_size=size, price=price)
            self.__all_orders__.push(new_order)
            return new_order
        return None
    
    def add_ask_order(self, size: float, price: float, timenow: int = None) -> bool:
        """
        size : float > 0
        price: float > 0
        timenow: integer > 0 | None, if none it is generated using epoch time
        assertions will be used
        """
        if self.__check_order_params__(size, price, timenow):
            if not timenow:
                timenow = int(time.time())
            new_order = Order(time=timenow, side=Side.SELL, order_size=size, price=price)
            self.__all_orders__.push(new_order)
            return new_order
        return None
    
    def fill_available_orders(self):
        market_state = self.get_market_state()
        for order in self.get_all_orders():
            if order.order.price == market_state.price:
                self.execute_order(order)

    def execute_order(self, order: OrderWrapper):
        # Execute the order (fill it)
        if order.order.side == Side.BUY:
            self.__currency_manager__.fill_order(order.order_size)
        else:
            self.__currency_manager__.fill_order(-1*order.order_size)
        # Remove the order from the order book
        self.__all_orders__.remove(order.order_id)
