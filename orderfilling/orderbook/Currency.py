from orderfilling.orderbook.dataclasses.CurrencyState import CurrencyState
# coinprice = totalmarketvalue/coinsincirculation
class Currency:

    def __init__(self, total_market_value: float = 0.0, available_liquidity: float = 0.0):
        self.__total_market_value__ = total_market_value
        self.__available_liquidity__ = available_liquidity
        self._initialized = True

    def __mutate_available_liquidity__(self, coins: float) -> None:
        self.__available_liquidity__ = self.__available_liquidity__ + coins
        return

    def __mutate_total_market_value__(self, value: float) -> None:
        self.__total_market_value__ = self.__total_market_value__ + value
        return
    
    def get_state(self, verbose:bool = False) -> CurrencyState:
        """
        verbose: prints state of currency, defaults to False
        """
        if verbose:
            print(f"Total Mkt Value: {self.__total_market_value__}")
            print(f"Total Coins in Circulation: {self.__available_liquidity__}")
            print(f"Coin Price: {self.get_coin_price()}")
        return CurrencyState(self.__total_market_value__, self.__available_liquidity__, self.get_coin_price())

    def get_coin_price(self) -> float:
        return self.__total_market_value__/self.__available_liquidity__
    
    def fill_order(self, coins:float) -> bool:
        """
        buy order: coins are positive
        sell order: coins are negative
        """
        # when buy order is filled, increase total market value, decrease coins in circulation
        # first get the price of total coins
        if coins == 0:
            return False  # No order to fill
        
        price = self.get_coin_price()

        if coins > 0:
            # Buy order
            total_value = price * coins
            self.__mutate_total_market_value__(total_value)
            self.__mutate_available_liquidity__(-coins)
        else:
            # Sell order
            total_value = price * abs(coins)
            self.__mutate_total_market_value__(-total_value)
            self.__mutate_available_liquidity__(-coins)
        
        return True
# following singleton pattern to maintain state between other files
currency: Currency = Currency(500, 5)