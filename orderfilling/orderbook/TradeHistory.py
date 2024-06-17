from dataclasses import dataclass

@dataclass
class Trade:
    executed_price: float
    volume: float
    executed_time: int # in epoch time

class TradeHistory:
    def __init__(self):
        self.trade_history = []
        self.limit = 100 # base price off of past 100 trades

    def add_trade(self, executed_price:float, volume:float, executed_time:int) -> None:
        self.trade_history.append(Trade(executed_price, volume, executed_time))
        if len(self.trade_history) > self.limit:
            self.trade_history.pop()
    
    def calculate_vwap(self):
        numerator = 0
        denominator = 0
        for trades in self.trade_history:
            numerator += trades.price * trades.volume
            denominator += trades.volume
        return numerator/denominator 
