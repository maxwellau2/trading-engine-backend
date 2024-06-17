import unittest
from orderfilling.orderbook.Currency import Currency
from orderfilling.orderbook.PriorityQueue import PriorityQueue
from orderfilling.orderbook.TradeHistory import TradeHistory
from orderfilling.orderbook.Orderbook import OrderBook
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, Side
from orderfilling.orderbook.dataclasses.CurrencyState import CurrencyState
import time

class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.pq = PriorityQueue()

    def test_push_orders(self):
        order1 = Order(time=int(time.time()), side=Side.BUY, order_size=100, price=50)
        order2 = Order(time=int(time.time()), side=Side.BUY, order_size=150, price=60)
        order3 = Order(time=int(time.time()), side=Side.BUY, order_size=50, price=50)
        
        self.pq.push(order1)
        self.pq.push(order2)
        self.pq.push(order3)
        
        self.assertEqual(len(self.pq), 3)
        self.assertEqual(self.pq.sorted_orders[0].price, 60)  # Highest price first for BUY

    def test_pop_order(self):
        order1 = Order(time=int(time.time()), side=Side.BUY, order_size=100, price=50)
        order2 = Order(time=int(time.time()), side=Side.BUY, order_size=150, price=60)
        
        self.pq.push(order1)
        self.pq.push(order2)
        
        popped_order = self.pq.pop()
        self.assertEqual(popped_order.price, 50)
        self.assertEqual(len(self.pq), 1)

    def test_peek_order(self):
        order = Order(time=int(time.time()), side=Side.BUY, order_size=100, price=50)
        self.pq.push(order)
        self.assertEqual(self.pq.peek().price, 50)

    def test_remove_order(self):
        order1 = Order(time=int(time.time()), side=Side.BUY, order_size=100, price=50)
        order2 = Order(time=int(time.time()), side=Side.BUY, order_size=150, price=60)
        
        self.pq.push(order1)
        self.pq.push(order2)
        
        self.pq.remove(order1.order_id)
        self.assertEqual(len(self.pq), 1)
        self.assertEqual(self.pq.sorted_orders[0].price, 60)

    def test_update_volume(self):
        order1 = Order(time=int(time.time()), side=Side.BUY, order_size=100, price=50)
        self.pq.push(order1)
        self.pq.update_volume(order1.order_id, 50)
        self.assertEqual(self.pq.sorted_orders[0].order_size, 50)

    def test_is_empty(self):
        self.assertTrue(self.pq.is_empty())
        order = Order(time=int(time.time()), side=Side.BUY, order_size=100, price=50)
        self.pq.push(order)
        self.assertFalse(self.pq.is_empty())

class TestOrderBook(unittest.TestCase):
    def setUp(self):
        self.order_book = OrderBook("TestBook", 1000000, 500000)

    def test_add_bid_order(self):
        bid_order = self.order_book.add_bid_order(100, 50)
        self.assertEqual(len(self.order_book.get_bids()), 1)
        self.assertEqual(self.order_book.get_bids()[0].price, 50)
    
    def test_add_ask_order(self):
        ask_order = self.order_book.add_ask_order(100, 60)
        self.assertEqual(len(self.order_book.get_asks()), 1)
        self.assertEqual(self.order_book.get_asks()[0].price, 60)
    
    def test_market_state(self):
        state = self.order_book.get_market_state()
        self.assertIsInstance(state, CurrencyState)
    
    def test_bid_ask_spread(self):
        self.order_book.add_bid_order(100, 50)
        self.order_book.add_ask_order(100, 60)
        spread = self.order_book.get_bid_ask_spread()
        self.assertEqual(spread, 10)
    
    def test_mid_price(self):
        self.order_book.add_bid_order(100, 50)
        self.order_book.add_ask_order(100, 60)
        mid_price = self.order_book.get_mid_price()
        self.assertEqual(mid_price, 55)

    def test_fill_available_orders(self):
        bid_order = self.order_book.add_bid_order(100, 50)
        ask_order = self.order_book.add_ask_order(100, 50)
        self.order_book.fill_available_orders()
        
        # After matching, there should be no bids or asks at the matched price.
        self.assertEqual(len(self.order_book.get_bids()), 0)
        self.assertEqual(len(self.order_book.get_asks()), 0)

if __name__ == '__main__':
    unittest.main()
