from dataclasses import dataclass
from typing import List


@dataclass
class Trade:
    executed_price: float
    volume: float
    executed_time: int  # in epoch time


class TradeHistory:
    def __init__(self):
        self.trade_history: List[Trade] = []
        self.trade_history_buffer : List[Trade] = []
        self.limit = 100  # base price off of past 100 trades
        self.buffer_limit = 200

    def add_trade(
        self, executed_price: float, volume: float, executed_time: int
    ) -> None:
        self.trade_history.append(Trade(executed_price, volume, executed_time))
        if len(self.trade_history) >= self.limit:
            self.trade_history_buffer.append(self.trade_history.pop())
        if len(self.trade_history_buffer) >= self.buffer_limit:
            # store to DB
            # refer to https://www.youtube.com/watch?v=p8tnmEdeOU0
            pass

    # def get_current_window_volume(self):

    def calculate_vwap(self):
        if len(self.trade_history) == 0:
            return 0
        numerator = 0
        denominator = 0
        for trades in self.trade_history:
            numerator += trades.executed_price * trades.volume
            denominator += trades.volume
        return numerator / denominator
