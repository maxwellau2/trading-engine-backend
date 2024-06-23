from orderfilling.orderbook.PriorityQueue import PriorityQueue
from orderfilling.orderbook.TradeHistory import TradeHistory
from orderfilling.orderbook.Orderbook import OrderBook
from orderfilling.orderbook.dataclasses.OrderDataClass import Order, Side
import time

# q = PriorityQueue()
# q.push(Order(Side.BUY, int(time.time()), 10, 10))
# q.push(Order(Side.BUY, int(time.time()), 20, 10))
# q.push(Order(Side.BUY, int(time.time()), 30, 10))
# q.push(Order(Side.BUY, int(time.time()), 10, 10))
# q.push(Order(Side.BUY, int(time.time()), 20, 10))
# q.push(Order(Side.BUY, int(time.time()), 30, 10))

# print(q.order_id_to_index)

# print([(x) for x in q.sorted_orders])

book = OrderBook("test")

book.add_ask_order(10, 10.000000000000001,None)
book.add_bid_order(10, 10.0001,None)
book.add_bid_order(10, 25.3,None)
book.add_ask_order(20, 25.3,None)
book.fill_available_orders()
book.fill_available_orders()
print(book.get_all_orders())
print(book.get_vwap_price())
print(book.get_all_orders())
