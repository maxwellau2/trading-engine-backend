from typing import List
from orderfilling.orderbook.dataclasses.OrderDataClass import Order


class PriorityQueue:
    def __init__(self):
        # priority q is sorted by
        # 1. Price
        # 2. Quantity
        # TODO 3. Time
        self.sorted_orders: List[Order] = []
        self.order_id_to_index = {}  # Dictionary to store order ID to index mapping

    def push(self, order: Order):
        index = self._binary_search(order.price)  # Find the appropriate index price wise
        while index < len(self.sorted_orders) and self.sorted_orders[index].price == order.price:
            # price collision, compare quantity size
            if self.sorted_orders[index].order_size > order.order_size:
                index += 1
            else:
                break
        self.sorted_orders.insert(index, order)  # Insert the order at the index
        self._update_order_id_to_index(index)  # Update the order ID to index mapping
        return

    def pop(self) -> Order:
        return self.sorted_orders.pop()

    def peek(self) -> Order:
        return self.sorted_orders[0] if self.sorted_orders else None

    def remove(self, order_id: str) -> bool:
        print(self.order_id_to_index)
        if order_id in self.order_id_to_index:
            index = self.order_id_to_index[order_id]
            del self.order_id_to_index[order_id]  # Remove the mapping
            del self.sorted_orders[index]  # Remove the order from the sorted_orders
            self._update_order_id_to_index(index)  # Update the mapping for other orders
            return True
        return False

    def _binary_search(self, price: float) -> int:
        # Perform binary search to find the appropriate index for insertion based on price
        left, right = 0, len(self.sorted_orders)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_orders[mid].price < price:
                right = mid
            else:
                left = mid + 1
        return left

    def _update_order_id_to_index(self, start_index: int):
        # Update the order ID to index mapping for orders after the given index
        for i in range(start_index, len(self.sorted_orders)):
            self.order_id_to_index[self.sorted_orders[i].order_id] = i

    def __len__(self):
        return len(self.sorted_orders)

    def is_empty(self) -> bool:
        return len(self.sorted_orders) == 0
    
    def max_price(self) -> float:
        # since list is sorted, technically we can just read the first entry
        # return self.sorted_orders[0].price
        return max([x.price for x in self.sorted_orders])

    def min_price(self) -> float:
        # since list is sorted, technically we can just read the last entry
        # return self.sorted_orders[-1].price
        return min([x.price for x in self.sorted_orders])

    
    def update_volume(self, order_id, new_volume):
        if order_id not in self.order_id_to_index:
           raise "Order ID not in dict"
        # if new volume is 0, remove it completely
        if new_volume == 0:
            self.remove(order_id)
        # update the volume if there is partial order left
        else:
            print(self.order_id_to_index)
            idx : int = self.order_id_to_index[order_id]
            self.sorted_orders[idx].order_size = new_volume
            return 
