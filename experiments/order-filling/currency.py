# coinprice = totalmarketvalue/coinsincirculation
class Currency:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Currency, cls).__new__(cls)
        return cls._instance

    def __init__(self, total_market_value: float = 0.0, coins_available: float = 0.0):
        if not hasattr(self, '_initialized'):  # Ensure __init__ is called only once
            self.__total_market_value__ = total_market_value
            self.__coins_available__ = coins_available
            self._initialized = True

    def __mutate_coins_available__(self, coins: float) -> None:
        self.__coins_available__ = self.__coins_available__ + coins
        return

    def __mutate_total_market_value__(self, value: float):
        self.__total_market_value__ = self.__total_market_value__ + value
        return
    
    def get_state(self, verbose:bool = False):
        """
        verbose: prints state of currency, defaults to False
        """
        if verbose:
            print(f"Total Mkt Value: {self.__total_market_value__}")
            print(f"Total Coins in Circulation: {self.__coins_available__}")
            print(f"Coin Price: {self.get_coin_price()}")
        return {
            "total_market_value": self.__total_market_value__,
            "coins_available": self.__coins_available__,
            "coin_price": self.get_coin_price()
        }

    def get_coin_price(self) -> float:
        return self.__total_market_value__/self.__coins_available__
    
    def fill_order(self, coins:float) -> bool:
        """
        buy order: coins are positive
        sell order: coins are negative
        """
        # when buy order is filled, increase total market value, decrease coins in circulation
        # first get the price of total coins
        price = self.get_coin_price()
        total_value = price * coins
        self.__mutate_total_market_value__(total_value)
        self.__mutate_coins_available__(-1*coins)
        return True

# following singleton pattern to maintain state between other files
currency: Currency = Currency(500, 5)