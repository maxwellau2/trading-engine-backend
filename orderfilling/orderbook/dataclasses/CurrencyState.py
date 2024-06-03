from dataclasses import dataclass
import numpy as np

@dataclass
class CurrencyState:
    market_value: np.double
    available_liquidity: np.double
    price : np.double