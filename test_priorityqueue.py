import unittest
from unittest.mock import patch
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, Side
from orderfilling.orderbook.PriorityQueue import PriorityQueue


class TestPriorityQueue(unittest.TestCase):
    def setUp(self):
        self.priority_queue = PriorityQueue()
        self.order1 = Order(side=Side.BUY, time=1, order_size=10.0, price=200.0)
        self.order2 = Order(side=Side.SELL, time=2, order_size=15.0, price=300.0)
        self.order3 = Order(side=Side.BUY, time=3, order_size=20.0, price=250.0)
        self.order4 = Order(side=Side.SELL, time=4, order_size=25.0, price=350.0)
        self.order1.order_id = "1"
        self.order2.order_id = "2"
        self.order3.order_id = "3"
        self.order4.order_id = "4"
        self.priority_queue.push(self.order1)
        self.priority_queue.push(self.order2)
        self.priority_queue.push(self.order3)
        self.priority_queue.push(self.order4)

    def test_push_and_pop(self):
        self.assertEqual(len(self.priority_queue), 4)
        self.assertEqual(self.priority_queue.peek(), self.order1)
        self.assertEqual(self.priority_queue.pop(), self.order4)
        self.assertEqual(len(self.priority_queue), 3)
        self.assertEqual(self.priority_queue.pop(), self.order3)
        self.assertEqual(len(self.priority_queue), 2)

    def test_remove(self):
        self.assertTrue(self.priority_queue.remove("2"))
        self.assertEqual(len(self.priority_queue), 3)
        self.assertEqual(self.priority_queue.peek(), self.order1)
        self.assertTrue(self.priority_queue.remove("1"))
        self.assertEqual(len(self.priority_queue), 2)
        self.assertEqual(self.priority_queue.peek(), self.order3)
        self.assertFalse(self.priority_queue.remove("5"))  # Non-existent order ID

    def test_peek(self):
        self.assertEqual(self.priority_queue.peek(), self.order1)
        self.priority_queue.pop()
        self.assertEqual(self.priority_queue.peek(), self.order1)

    def test_is_empty(self):
        self.assertFalse(self.priority_queue.is_empty())
        self.priority_queue.pop()
        self.priority_queue.pop()
        self.priority_queue.pop()
        self.priority_queue.pop()
        self.assertTrue(self.priority_queue.is_empty())


if __name__ == "__main__":
    unittest.main()
