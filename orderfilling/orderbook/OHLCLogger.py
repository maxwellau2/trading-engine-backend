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

    def to_dict(self) -> dict:
        return {
            "time": self.time,
            "open": self.open,
            "high": self.high,
            "low": self.low,
            "close": self.close,
            "volume": self.volume
        }


class OHLCVLogger:
    def __init__(self, interval: int = 300):  # 5-minute interval
        self.interval = interval
        self.ohlcv: List[OHLCV] = []
        self.current_candle = None

    def _create_new_candle(self, timestamp: int, price: float, volume: float):
        start_time = (timestamp // self.interval) * self.interval
        self.current_candle = OHLCV(
            time=start_time,
            open=price,
            high=price,
            low=price,
            close=price,
            volume=volume
        )

    def update(self, timestamp: int, price: float, volume: float):
        if not self.current_candle or timestamp >= self.current_candle.time + self.interval:
            if self.current_candle:
                self._finalize_current_candle()
            self._create_new_candle(timestamp, price, volume)
        else:
            self._update_current_candle(price, volume)

    def _update_current_candle(self, price: float, volume: float):
        self.current_candle.high = max(self.current_candle.high, price)
        self.current_candle.low = min(self.current_candle.low, price)
        self.current_candle.close = price
        self.current_candle.volume += volume

    def _finalize_current_candle(self):
        self.ohlcv.append(self.current_candle)
        self.current_candle = None

    def get_ohlcv(self) -> List[OHLCV]:
        if self.current_candle:
            # self._finalize_current_candle()
            return [candle.to_dict() for candle in self.ohlcv] + [self.current_candle.to_dict()]
        return [candle.to_dict() for candle in self.ohlcv]
