from dataclasses import dataclass
from enum import Enum
import uuid
import numpy as np

class Side(Enum):
    BUY = 1
    SELL = -1


@dataclass
class Order:
    time: np.uint # time is defined in epoch time
    order_id: str
    side: Side
    order_size: np.double
    price: np.double

    def __init__(self, side: Side, time: int, order_size: float, price: float):
        self.order_id = str(uuid.uuid4())
        self.side = side
        self.time = time
        self.order_size = order_size
        self.price = price

    def __repr__(self) -> str:
        return self.__dict__


class OrderWrapper:
    def __init__(self, order: Order):
        self.order = order

    def __lt__(self, other):
        # Compare by time first (FIFO), then by order_size (negative to make it max-heap by quantity)
        if self.order.time == other.order.time:
            return self.order.order_size > other.order.order_size
        return self.order.time < other.order.time
    
    def __repr__(self) -> str:
        return f"{id : {self.order.order_id}, time : {self.order.time}, size : {self.order.order_size}, price : {self.order.price}}"