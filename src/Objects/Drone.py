class Drone:
    def __init__(self, index, position, stock=[]):
        self.index: int = index  # Represents the index of the drone
        self.position: tuple[int, int] = position
        self.stock: list[int] = stock
        self.totalLoad: int = 0
