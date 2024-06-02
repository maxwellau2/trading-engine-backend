# we will use class composition to define the orderbook
# it is composed of the Currency class as defined in Currency.py
from orderfilling.orderbook.Currency import Currency
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, Side
from orderfilling.orderbook.dataclasses.CurrencyState import CurrencyState

class OrderBook:
    def __init__(self, name:str, total_market_value:float, available_liquidity:float) -> None:
        self.name = name
        self.__currency_manager__ = Currency(total_market_value=total_market_value, available_liquidity=available_liquidity)
        self.__bids__ : list[Order] = []
        self.__asks__ : list[Order] = []

    def get_market_state(self) -> CurrencyState:
        return self.__currency_manager__.get_state()
    
    def get_bids(self):
        return self.__bids__
    
    def get_asks(self):
        return self.__asks__

    def get_all_orders(self):
        # just use arary concatenation
        return self.get_bids() + self.get_asks()
    
    def __check_order_params__(self, size:float, price:float) -> bool:
        assert (size > 0), "size has to be a positive integer"
        assert (price > 0), "side has to be a positive integer"
        return True
    
    def add_bid_order(self, size: float, price: float) -> bool:
        """
        size : float > 0
        price: float > 0
        assertions will be used
        """
        if self.__check_order_params__(size, price):
            new_order = Order(side=Side.BUY, order_size=size, price=price)
            self.__bids__.append(new_order)
            return True
        return False
    
    def add_ask_order(self, size: float, price: float) -> bool:
        """
        size : float > 0
        price: float > 0
        assertions will be used
        """
        if self.__check_order_params__(size, price):
            new_order = Order(side=Side.SELL, order_size=size, price=price)
            self.__asks__.append(new_order)
            return True
        return False
    
