from dataclasses import dataclass
from enum import Enum
import uuid
import numpy as np

class Side(Enum):
    BUY = 1
    SELL = -1

class Order:
    def __init__(self, side: Side, time: int, order_size: float, price: float):
        self.order_id = str(uuid.uuid4())
        self.side = side
        self.time = time
        self.order_size = order_size
        self.price = price
    def __lt__(self, other):
        # Compare by time first (FIFO), then by order_size (negative to make it max-heap by quantity)
        if self.time == other.time:
            return self.order_size > other.order_size
        return self.order.time < other.order.time
    
    def __repr__(self) -> str:
        return f"Order(id={self.order_id}, side={self.side.name}, time={self.time}, size={self.order_size}, price={self.price})"
    
    