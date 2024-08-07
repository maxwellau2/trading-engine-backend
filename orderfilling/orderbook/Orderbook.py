from typing import List, Tuple
from orderfilling.orderbook.PriorityQueue import PriorityQueue
from orderfilling.orderbook.TradeHistory import TradeHistory
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, Side
import time
from orderfilling.orderbook.OHLCLogger import OHLCV, OHLCVLogger


class OrderBook:
    def __init__(self, name: str) -> None:
        self.name = name
        # self.__all_orders__ = PriorityQueue()
        self.__bid_orders__ = PriorityQueue()
        self.__ask_orders__ = PriorityQueue()
        self.__trade_history__ = TradeHistory()
        self.__ohlcv_data__ = OHLCVLogger(interval=60)

    def get_bids(self) -> List[Order]:
        return self.__bid_orders__.sorted_orders

    def get_asks(self) -> List[Order]:
        return self.__ask_orders__.sorted_orders

    def get_all_orders(self) -> List[Order]:
        """
        returns a sorted list of Orders, including bids and asks
        """
        return [x.to_dict() for x in self.__ask_orders__.sorted_orders] + [x.to_dict() for x in self.__bid_orders__.sorted_orders]

    def __check_order_params__(
        self, size: float, price: float, timenow: int | None
    ) -> bool:
        assert size > 0, "size has to be a positive integer"
        assert price > 0, "side has to be a positive integer"
        assert price > 0, "side has to be a positive integer"
        assert timenow == None or timenow > 0, "time has to be None or positive"
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
            new_order = Order(time=timenow, side=Side.BUY, order_size=size, price=price, ticker=self.name)
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
            new_order = Order(
                time=timenow, side=Side.SELL, order_size=size, price=price, ticker=self.name
            )
            self.__ask_orders__.push(new_order)
            return new_order.to_dict()
        return None

    def get_bid_ask_spread(self) -> float:
        return self.__ask_orders__.min_price() - self.__bid_orders__.max_price()

    def get_mid_price(self) -> float:
        return (self.__ask_orders__.min_price() + self.__bid_orders__.max_price()) / 2

    def get_vwap_price(self) -> float:
        return self.__trade_history__.calculate_vwap()

    def fill_available_orders(self):
        # check wrt bids
        for bid in self.get_bids():
            for ask in self.get_asks():
                if bid.price == ask.price:
                    remaining = self.execute_trade(bid, ask)
                    # update the order book, supports partial fills
                    self.__bid_orders__.update_volume(bid.order_id, remaining[0])
                    self.__ask_orders__.update_volume(ask.order_id, remaining[1])

    def get_trade_history(self):
        return self.__trade_history__.get_serialized_history()

    def execute_trade(self, bid: Order, ask: Order) -> Tuple[float, float]:
        """
        returns a tuple of [remaining bid, remaining ask] volumes, supports partial fills
        """
        timestamp = int(time.time())
        trade_price = ask.price if bid.order_size >= ask.order_size else bid.price
        trade_volume = min(bid.order_size, ask.order_size)
        self.__ohlcv_data__.update(timestamp, trade_price, trade_volume)
        if bid.order_size > ask.order_size:
            self.__trade_history__.add_trade(
                executed_price=ask.price, volume=ask.order_size, executed_time=int(time.time()), ticker=self.name,
            )
            return (bid.order_size - ask.order_size, 0)
        elif bid.order_size < ask.order_size:
            self.__trade_history__.add_trade(
                executed_price=bid.price, volume=bid.order_size, executed_time=int(time.time()), ticker=self.name,
            )
            return (0, ask.order_size - bid.order_size)
        else:
            self.__trade_history__.add_trade(
                executed_price=bid.price, volume=bid.order_size, executed_time=int(time.time()), ticker=self.name,
            )
            return (0, 0)

    def get_ohlcv_data(self) -> List[OHLCV]:
        return self.__ohlcv_data__.get_ohlcv()