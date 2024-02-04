from Objects.Order import Order


class Warehouse:
    def __init__(
            self,
            index: int,
            position: tuple[int, int],
            stock: list[int]
    ):
        self.index = index  # Represents the index of the warehouse
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock  # Warehouse stocks
        self.nearest_orders = list[Order]

    def is_empty(self):
        """Return True if a warehouse is empty"""
        return self.stock == [0 for i in range(len(self.stock))]
