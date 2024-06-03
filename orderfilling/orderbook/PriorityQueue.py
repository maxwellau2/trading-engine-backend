from orderfilling.orderbook.dataclasses.OrderDataClass import Order, OrderWrapper


class PriorityQueue:
    def __init__(self):
        self.sorted_orders = []
        self.order_id_to_index = {}  # Dictionary to store order ID to index mapping

    def push(self, order: Order):
        index = self._binary_search(order.time)  # Find the appropriate index
        while index < len(self.sorted_orders) and self.sorted_orders[index].order.time == order.time:
            # Time collision, compare quantity size
            if self.sorted_orders[index].order.order_size > order.order_size:
                index += 1
            else:
                break
        self.sorted_orders.insert(index, OrderWrapper(order))  # Insert the order at the index
        self._update_order_id_to_index(index)  # Update the order ID to index mapping
        return

    def pop(self) -> Order:
        return self.sorted_orders.pop().order

    def peek(self) -> Order:
        return self.sorted_orders[0].order if self.sorted_orders else None

    def remove(self, order_id: str) -> bool:
        if order_id in self.order_id_to_index:
            index = self.order_id_to_index[order_id]
            del self.order_id_to_index[order_id]  # Remove the mapping
            del self.sorted_orders[index]  # Remove the order from the sorted_orders
            self._update_order_id_to_index(index)  # Update the mapping for other orders
            return True
        return False

    def _binary_search(self, time: int) -> int:
        # Perform binary search to find the appropriate index for insertion
        left, right = 0, len(self.sorted_orders)
        while left < right:
            mid = (left + right) // 2
            if self.sorted_orders[mid].order.time < time:
                left = mid + 1
            else:
                right = mid
        return left

    def _update_order_id_to_index(self, start_index: int):
        # Update the order ID to index mapping for orders after the given index
        for i in range(start_index, len(self.sorted_orders)):
            self.order_id_to_index[self.sorted_orders[i].order.order_id] = i

    def __len__(self):
        return len(self.sorted_orders)

    def is_empty(self) -> bool:
        return len(self.sorted_orders) == 0
