# we will use class composition to define the orderbook
# it is composed of the Currency class as defined in Currency.py
from typing import List, Tuple
from orderfilling.orderbook.Currency import Currency
from orderfilling.orderbook.PriorityQueue import PriorityQueue
from orderfilling.orderbook.TradeHistory import TradeHistory
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, Side
from orderfilling.orderbook.dataclasses.CurrencyState import CurrencyState
import numpy as np
import time

class OrderBook:
    def __init__(self, name:str, total_market_value:float, available_liquidity:float) -> None:
        self.name = name
        self.__currency_manager__ = Currency(total_market_value=total_market_value, available_liquidity=available_liquidity)
        self.__all_orders__ = PriorityQueue()
        self.__bid_orders__ = PriorityQueue()
        self.__ask_orders__ = PriorityQueue()
        self.__trade_history__ = TradeHistory()

    def get_market_state(self) -> CurrencyState:
        return self.__currency_manager__.get_state()
    
    def get_bids(self) -> List[Order]:
        # return [order for order in self.__all_orders__.sorted_orders if order.side == Side.BUY]
        return self.__bid_orders__.sorted_orders
    
    def get_asks(self) -> List[Order]:
        # return [order for order in self.__all_orders__.sorted_orders if order.side == Side.SELL]
        return self.__ask_orders__.sorted_orders
    

    def get_all_orders(self) -> List[Order]:
        """
        returns a sorted list of Orders, including bids and asks
        """
        # return self.__all_orders__.sorted_orders
        return self.__ask_orders__.sorted_orders + self.__bid_orders__.sorted_orders
    
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
            self.__bid_orders__.push(new_order)
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
            self.__ask_orders__.push(new_order)
            return new_order
        return None
    
    def get_bid_ask_spread(self) -> float:
        return min(self.get_asks()) - max(self.get_bids())
    
    def get_mid_price(self) -> float:
        return (min(self.get_asks()) + max(self.get_bids())) / 2
    
    # def get_vwap_price(self) -> float:

    
    def fill_available_orders(self):
        # check wrt bids
        for bid in self.get_bids():
            for ask in self.get_asks():
                if bid.price == ask.price:
                    remaining = self.execute_trade(bid, ask)
                    bid.order_size = remaining[0]
                    ask.order_size = remaining[1]
                    if bid.order_size == 0:
                        self.__bid_orders__.remove(bid.order_id)
                    if ask.order_size == 0:
                        self.__ask_orders__.remove(ask.order_id)

    def execute_trade(self, bid: Order, ask: Order) -> Tuple[float, float]:
        if bid.order_size > ask.order_size:
            self.__trade_history__.add_trade(ask.price, ask.order_size, int(time.now()))
            return (bid.order_size - ask.order_size, 0)
        elif bid.order_size < ask.order_size:
            self.__trade_history__.add_trade(bid.price, bid.order_size, int(time.now()))
            return (ask.order_size- bid.order_size, 0)
        else:
            self.__trade_history__.add_trade(bid.price, bid.order_size, int(time.now()))
            return (0,0)

    # def execute_order(self, order: Order):
    #     # Execute the order (fill it)
    #     if order.side == Side.BUY:
    #         self.__currency_manager__.fill_order(order.order_size)
    #     else:
    #         self.__currency_manager__.fill_order(-1*order.order_size)
    #     # Remove the order from the order book
    #     self.__all_orders__.remove(order.order_id)
