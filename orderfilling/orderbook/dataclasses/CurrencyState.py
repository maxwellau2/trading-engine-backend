from dataclasses import dataclass

@dataclass
class CurrencyState:
    market_value: float
    available_liquidity: float
    price : float