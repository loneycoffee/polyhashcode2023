from polyparser import parse_challenge
from utils.functs import (
    rank_orders_by_weight,
    create_clusters,
    find_closest_warehouse,
    max_qty_allowed_to_load,
    makeCommand,
    update_ranking_score_clusters,
    find_best_cluster,
    find_closest_cluster_to_obj,
)

from typing import List


def naive_approach_theo(challenge: str) -> List[str]:
    """
    The idea is to create clusters of closest orders
    and then to complete each cluster.

    We use a system of ranking to sort the best clusters by
    the weight coefficient and distance coefficient.

    For each cluster we complete each order one by one by looking
    at the nearest warehouse with the needed quantity.

    When we complet a cluster we choose the best cluster
    and we repeat the process until there is no more clusters.
    """
    # Initialization
    solution = []
    challenge = parse_challenge(challenge)

    WEIGHTCOEFF = 0.9  # The importance of weight in the ranking
    DISTCOEFF = 0.1  # The importance of distance in the ranking
    IDEAL_CLUSTER_SIZE = 2  # 2 is the best for now

    orders = challenge.orders

    # Ranking orders by weight
    orders = rank_orders_by_weight(challenge, orders)

    # Creating clusters
    clusters = create_clusters(challenge, orders, WEIGHTCOEFF, DISTCOEFF,
                               IDEAL_CLUSTER_SIZE)

    # Completing orders for each cluster
    # The first cluster chosen is the one with the highest ranking score
    cluster_id = find_closest_cluster_to_obj(
        challenge, challenge.warehouses[0], clusters)

    # We iterate through the drones to complete the clusters
    drone_index = 0
    while len(clusters) > 0:  # While there is clusters to complete

        # We choose the drone index
        if drone_index + 1 > len(challenge.drones) - 1:
            drone_index = 0
        else:
            drone_index += 1
        drone = challenge.drones[drone_index]

        # We fetch the cluster with its id
        cluster = clusters[cluster_id]
        # We create a copy of the cluster
        # that we are going to use to calculate
        # the next cluster
        tmp_cluster = cluster.copy_cluster()

        # While there is orders to complete in the cluster
        while not cluster.are_orders_full_filled():
            # We fetch the first order of the cluster
            order = cluster.get_first_order()
            # While the order is not completed
            while not order.check_full_filled():
                # The idea is to load fully the drone each time
                # to try to optimize the number of turns used

                # We iterate through the products of the order
                for product_type, qty_order in enumerate(order.products_qty):

                    if qty_order > 0:  # If we need the product
                        # We look at how much we can load with the drone
                        max_qty_able_load = max_qty_allowed_to_load(
                            challenge, drone, product_type
                        )

                        # We choose the quantity to load
                        # if the drone can take more than the order needs
                        # we take the quantity needed
                        # else we take the max quantity the drone can take
                        qty = min(qty_order, max_qty_able_load)
                        if qty > 0:
                            warehouse, qty = find_closest_warehouse(
                                challenge,
                                drone.index,
                                product_type,
                                qty
                            )

                            # We move the drone to the warehouse
                            drone.position = warehouse.position

                            # We load the drone for the solution
                            makeCommand(
                                "L",
                                solution,
                                drone.index,
                                warehouse.index,
                                product_type,
                                qty,
                            )
                            # We update the stock of the drone
                            # and the warehouse
                            drone.stock[product_type] += qty
                            warehouse.stock[product_type] -= qty

                # We move the drone to the order
                drone.position = order.position
                for product_type, qty_prod in enumerate(drone.stock):
                    # if the drone has the product needed
                    if qty_prod > 0:
                        # We deliver the product
                        makeCommand(
                            "D",
                            solution,
                            drone.index,
                            order.index,
                            product_type,
                            qty_prod
                        )
                        order.products_qty[product_type] -= qty_prod
                        drone.stock[product_type] -= qty_prod

            # We remove the order from the cluster
            cluster.del_order_full_filled(order)
            # The next order will be the first of the cluster

        # Once we are done with the cluster
        # We calculate the ranking score for each cluster
        # and we choose the best cluster to go to
        del clusters[cluster_id]
        if len(clusters) - 1 >= 0:
            # Updating the ranking score for all clusters (distance changes)
            clusters = update_ranking_score_clusters(
                challenge, tmp_cluster, clusters)

            # We choose the best cluster according to the ranking
            cluster_id = find_best_cluster(clusters)

    return solution
