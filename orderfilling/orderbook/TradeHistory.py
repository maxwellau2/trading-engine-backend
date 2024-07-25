from dataclasses import dataclass
import time
from typing import List
from orderfilling.api.models.TradeModel import TradeDB
from orderfilling.orderbook.dataclasses.OrderDataClass import Side
import uuid


@dataclass
class Trade:
    ticker: str
    executed_price: float
    volume: float
    executed_time: int  # in epoch time
    trade_id: str = str(uuid.uuid4())  # uuid

    def to_dict(self) -> dict:
        return {
            "trade_id": str(self.trade_id),
            "executed_price" : self.executed_price,
            "volume": self.volume,
            "executed_time": self.executed_time,
            "ticker": self.ticker
        }


class TradeHistory:
    def __init__(self):
        self.trade_history: List[Trade] = []
        self.trade_history_buffer: List[Trade] = []
        self.limit = 100  # base price off of past 100 trades
        self.buffer_limit = 200

    def add_trade(
        self, executed_price: float, volume: float, executed_time: int, ticker: str,
    ) -> None:
        self.trade_history.append(Trade(trade_id=str(uuid.uuid4()), executed_price=executed_price, volume=volume, executed_time=executed_time, ticker=ticker))
        if len(self.trade_history) >= self.limit:
            self.trade_history_buffer.append(self.trade_history.pop())
        if len(self.trade_history_buffer) >= self.buffer_limit:
            # store to DB
            # refer to https://www.youtube.com/watch?v=p8tnmEdeOU0
            # pass
            result: Trade =self.trade_history_buffer.pop()
            TradeDB.create(trade_id=result.trade_id, ticker=ticker, qty=result.volume, price=result.executed_price, created_at=int(time.time()))

    def get_serialized_history(self) -> List[dict]:
        if not self.trade_history:
            return []
        print(self.trade_history)
        return [trade.to_dict() for trade in self.trade_history]

    def calculate_vwap(self):
        if len(self.trade_history) == 0:
            return 0
        numerator = 0
        denominator = 0
        for trades in self.trade_history:
            numerator += trades.executed_price * trades.volume
            denominator += trades.volume
        return numerator / denominator
