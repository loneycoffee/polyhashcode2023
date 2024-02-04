from copy import deepcopy
from Objects import Order


class Cluster:

    # We define a class for our cluster based algorithm
    # The idea is the group orders by proximity and make clusters or orders.
    def __init__(
            self,
            cluster_id: int,
            weight_coeff: float,
            dist_coeff: float
    ):

        self.cluster_id = cluster_id
        # To decide what is a "good" order we want to score every order
        # based on 2 differents factors :
        # its weight and its distance from an object (most likely a drone)
        self.weight_coeff = weight_coeff
        self.dist_coeff = dist_coeff

        self.orders = []

        self.weight_ranking = 0
        self.dist_ranking = 0
        self.score_ranking = 0

        self.position = None

    def calc_weight_ranking(self):
        """Calc the rank of the cluster based on it's orders weights."""
        self.weight_ranking = 0
        for order in self.orders:
            self.weight_ranking += order.weight_ranking

        self.weight_ranking /= len(self.orders)

    def append_orders(self, orders):
        """Add an order or a list of orders to a cluster"""
        if isinstance(orders, list):
            self.orders.extend(orders)
        else:
            self.orders.append(orders)
        if len(self.orders) > 0:
            self.calc_weight_ranking()
            self.position = self.orders[0].position

    def get_first_order(self):
        """Return the first order of a cluster"""
        if len(self.orders) > 0:
            return self.orders[0]

    def del_order_full_filled(self, order: Order):
        """Delete an order that is full filled"""
        # KNOWN BUG, SOMETIMES WE DELETE
        # NON-FULL-FILLED ORDERS IN THEO ALGORITHM
        # assert not order.check_full_filled()  # -> return an error
        self.orders.remove(order)

    def calc_score_ranking(self):
        """
        Calc the score of the cluster using its weight rank,
        dist rank and the differents coeffs
        """
        self.score_ranking = self.weight_ranking * self.weight_coeff + \
            self.dist_ranking * self.dist_coeff

    def calc_dist_ranking(self, dist_pos: list[int, int], nb_clusters: int):
        self.dist_ranking = (nb_clusters - dist_pos) / nb_clusters
        self.calc_score_ranking()

    def copy_cluster(self):
        return deepcopy(self)

    def are_orders_full_filled(self):
        return len(self.orders) == 0
