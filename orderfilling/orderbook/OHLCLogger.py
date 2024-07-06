from dataclasses import dataclass
import datetime
import time
from typing import List


@dataclass
class OHLCV:
    time: int
    open: float
    high: float
    low: float
    close: float
    volume: float


class OHLCVLogger:
    def __init__(self, initial_data: List[OHLCV] = [], limit: int = 200):
        self.history = initial_data
        self.buffer: List[OHLCV] = []
        self.storeable: List[OHLCV] = []
        self.limit = limit
        self.last_logged = time.time()
        self.current_window: OHLCV = (
            self.history[-1] if len(self.history) != 0 else OHLCV(0, 0, 0, 0, 0, 0)
        )

    def update_current_OHLC(self, current_price: float):
        if (time.time() - self.last_logged) >= 60:
            self.current_window.open = current_price
        if current_price > self.current_window.high:
            self.current_window.high = current_price
        if current_price < self.current_window.low:
            self.current_window.low = current_price
        self.current_window.close = current_price
        return

    def log(self, current_price: float):
        # check if current time is 1 minute away from previous time
        self.update_current_OHLC(current_price)
        if (time.time() - self.last_logged) >= 60:
            self.history.append(self.current_window)
            self.last_logged = time.time()
            print(f"logged at {time.time()}")
        return
