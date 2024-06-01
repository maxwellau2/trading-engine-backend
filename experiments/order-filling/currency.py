# coinprice = totalmarketvalue/coinsincirculation
class Currency:
    def __init__(self, total_market_value: float, coins_available: float):
        self.__total_market_value__ = total_market_value
        self.__coins_available__ = coins_available

    def __mutate_coins_available__(self, coins: float) -> None:
        self.__coins_available__ = self.__coins_available__ + coins
        return

    def __mutate_total_market_value__(self, value: float):
        self.__total_market_value__ = self.__total_market_value__ + value
        return
    
    def get_state(self):
        print(f"Total Mkt Value: {self.__total_market_value__}")
        print(f"Total Coins in Circulation: {self.__coins_available__}")
        print(f"Coin Price: {self.get_coin_price()}")

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

# Example usage
# fuck = Currency(500, 5)
# print(fuck.get_coin_price())
# fuck.get_state()
# fuck.fill_order(1)
# fuck.get_state()
# print(fuck.get_coin_price())