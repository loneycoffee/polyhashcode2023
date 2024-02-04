from math import sqrt, ceil

from Objects import Warehouse, Drone, Order


class Map:
    def __init__(
            self,
            rows: int,
            cols: int,
            nb_drones: int,
            nb_turns: int,
            max_payload: int,
            product_weights: list[int],
    ):
        self.rows: int = rows
        self.cols: int = cols
        self.nb_drones: int = nb_drones
        self.nb_turns: int = nb_turns
        self.max_payload: int = max_payload
        self.product_weights: list[int] = product_weights
        self.warehouses: list[Warehouse] = []
        self.drones: list[Drone] = []
        self.orders: list[Order] = []

    @staticmethod
    def calc_dist(object1, object2) -> int:
        """Return the integer distance from 2 objects"""
        return ceil(
            sqrt(
                (object2.position[0] - object1.position[0]) ** 2
                + (object2.position[1] - object1.position[1]) ** 2
            )
        )
