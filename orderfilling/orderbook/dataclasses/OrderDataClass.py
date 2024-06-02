from dataclasses import dataclass
from enum import Enum

class Side(Enum):
    BUY = 1
    SELL = -1


@dataclass
class Order:
    side: Side
    order_size: float
    price: float