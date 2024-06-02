import unittest
from orderfilling.orderbook.Orderbook import OrderBook
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, Side
from orderfilling.orderbook.dataclasses.CurrencyState import CurrencyState

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.orderbook = OrderBook(name="dog", total_market_value=1000, available_liquidity=10)

    def test_initial_market_state(self):
        state = self.orderbook.get_market_state()
        self.assertIsInstance(state, CurrencyState)
        self.assertEqual(state.market_value, 1000)
        self.assertEqual(state.available_liquidity, 10)

    def test_initial_orders(self):
        self.assertEqual(self.orderbook.get_bids(), [])
        self.assertEqual(self.orderbook.get_asks(), [])
        self.assertEqual(self.orderbook.get_all_orders(), [])

    def test_add_bid_order(self):
        result = self.orderbook.add_bid_order(1, 10)
        self.assertTrue(result)
        bids = self.orderbook.get_bids()
        self.assertEqual(len(bids), 1)
        self.assertEqual(bids[0].order_size, 1)
        self.assertEqual(bids[0].price, 10)
        self.assertEqual(bids[0].side, Side.BUY)

    def test_add_ask_order(self):
        result = self.orderbook.add_ask_order(1, 20)
        self.assertTrue(result)
        asks = self.orderbook.get_asks()
        self.assertEqual(len(asks), 1)
        self.assertEqual(asks[0].order_size, 1)
        self.assertEqual(asks[0].price, 20)
        self.assertEqual(asks[0].side, Side.SELL)

    def test_get_all_orders(self):
        self.orderbook.add_bid_order(1, 10)
        self.orderbook.add_ask_order(2, 20)
        all_orders = self.orderbook.get_all_orders()
        self.assertEqual(len(all_orders), 2)

    def test_invalid_bid_order(self):
        with self.assertRaises(AssertionError):
            self.orderbook.add_bid_order(-1, 10)

    def test_invalid_ask_order(self):
        with self.assertRaises(AssertionError):
            self.orderbook.add_ask_order(1, -10)

if __name__ == '__main__':
    unittest.main()
