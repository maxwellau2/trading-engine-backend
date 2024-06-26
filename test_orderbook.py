import unittest
import time
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, Side
from orderfilling.orderbook.dataclasses.CurrencyState import CurrencyState
from orderfilling.orderbook.Orderbook import OrderBook
import numpy as np


class TestOrderBook(unittest.TestCase):

    def setUp(self):
        self.order_book = OrderBook(
            name="TestOrderBook",
            total_market_value=1000000.0,
            available_liquidity=500000.0,
        )

    def test_initialization(self):
        self.assertEqual(self.order_book.name, "TestOrderBook")
        self.assertEqual(len(self.order_book.get_bids()), 0)
        self.assertEqual(len(self.order_book.get_asks()), 0)
        self.assertEqual(len(self.order_book.get_all_orders()), 0)

    def test_get_market_state(self):
        market_state = self.order_book.get_market_state()
        self.assertEqual(market_state.market_value, 1000000.0)
        self.assertEqual(market_state.available_liquidity, 500000.0)
        self.assertIsInstance(market_state.price, float)

    def test_add_bid_order(self):
        self.assertTrue(self.order_book.add_bid_order(size=10.0, price=100.0))
        bids = self.order_book.get_bids()
        self.assertEqual(len(bids), 1)
        self.assertEqual(bids[0].side, Side.BUY)
        self.assertEqual(bids[0].order_size, 10.0)
        self.assertEqual(bids[0].price, 100.0)

    def test_add_ask_order(self):
        self.assertTrue(self.order_book.add_ask_order(size=5.0, price=200.0))
        asks = self.order_book.get_asks()
        self.assertEqual(len(asks), 1)
        self.assertEqual(asks[0].side, Side.SELL)
        self.assertEqual(asks[0].order_size, 5.0)
        self.assertEqual(asks[0].price, 200.0)

    def test_get_all_orders(self):
        self.order_book.add_bid_order(size=10.0, price=100.0)
        self.order_book.add_ask_order(size=5.0, price=200.0)
        all_orders = self.order_book.get_all_orders()
        self.assertEqual(len(all_orders), 2)

    def test_fifo_and_quantity_priority_bids_different_time(self):
        self.order_book.add_bid_order(size=10.0, price=100.0)
        time.sleep(1)  # Ensure the next order has a different timestamp
        self.order_book.add_bid_order(size=15.0, price=100.0)
        self.order_book.add_bid_order(size=5.0, price=100.0)

        bids = self.order_book.get_bids()
        self.assertEqual(len(bids), 3)

        # Test FIFO: first order should be the one with size 10.0
        self.assertEqual(bids[0].order_size, 10.0)

        # Test quantity priority: next should be the one with size 15.0
        self.assertEqual(bids[1].order_size, 15.0)

        # Last should be the one with size 5.0
        self.assertEqual(bids[2].order_size, 5.0)

    def test_fifo_and_quantity_priority_asks_different_time(self):
        self.order_book.add_ask_order(size=10.0, price=200.0)
        time.sleep(1)  # Ensure the next order has a different timestamp
        self.order_book.add_ask_order(size=15.0, price=200.0)
        self.order_book.add_ask_order(size=5.0, price=200.0)

        asks = self.order_book.get_asks()
        self.assertEqual(len(asks), 3)

        # Test FIFO: first order should be the one with size 10.0
        self.assertEqual(asks[0].order_size, 10.0)

        # Test quantity priority: next should be the one with size 15.0
        self.assertEqual(asks[1].order_size, 15.0)

        # Last should be the one with size 5.0
        self.assertEqual(asks[2].order_size, 5.0)
        # print("different time",self.order_book.get_asks())

    def test_fifo_and_quantity_priority_bids(self):
        timenow = 1
        self.order_book.add_bid_order(size=10.0, price=100.0, timenow=timenow)
        self.order_book.add_bid_order(size=15.0, price=100.0, timenow=timenow)
        self.order_book.add_bid_order(size=5.0, price=100.0, timenow=timenow)

        bids = self.order_book.get_bids()
        self.assertEqual(len(bids), 3)

        # Test quantity priority: first should be the one with size 15.0
        self.assertEqual(bids[0].order_size, 15.0)

        # Next should be the one with size 10.0
        self.assertEqual(bids[1].order_size, 10.0)

        # Last should be the one with size 5.0
        self.assertEqual(bids[2].order_size, 5.0)
        # print("same time",self.order_book.get_bids())

    def test_fifo_and_quantity_priority_asks(self):
        timenow = 1
        self.order_book.add_ask_order(size=10.0, price=200.0, timenow=timenow)
        self.order_book.add_ask_order(size=15.0, price=200.0, timenow=timenow)
        self.order_book.add_ask_order(size=5.0, price=200.0, timenow=timenow)

        asks = self.order_book.get_asks()
        self.assertEqual(len(asks), 3)

        # Test quantity priority: first should be the one with size 15.0
        self.assertEqual(asks[0].order_size, 15.0)

        # Next should be the one with size 10.0
        self.assertEqual(asks[1].order_size, 10.0)

        # Last should be the one with size 5.0
        self.assertEqual(asks[2].order_size, 5.0)
        # print("same time",self.order_book.get_asks())

    def test_check_order_params(self):
        with self.assertRaises(AssertionError):
            self.order_book.add_bid_order(size=-1, price=100.0)
        with self.assertRaises(AssertionError):
            self.order_book.add_bid_order(size=10.0, price=-100.0)


if __name__ == "__main__":
    unittest.main()
