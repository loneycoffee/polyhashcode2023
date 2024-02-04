from Objects import Warehouse, Map, Order, Cluster, Drone
from typing import Tuple


def find_closest_warehouse(
        challenge: Map,
        drone_index: int,
        item_type: int,
        qty: int
) -> Tuple[Warehouse, int]:
    """
    Return the closest warehouse and the maximum
    qty possible to get in one load on the map.
    """
    best_warehouse = (-1, float('inf'))
    warehouses = challenge.warehouses

    while best_warehouse[0] == -1:
        for curr_warehouse in warehouses:
            if curr_warehouse.stock[item_type] >= qty:
                dist = challenge.calc_dist(
                    challenge.drones[drone_index],
                    curr_warehouse
                )
                if dist < best_warehouse[1]:
                    best_warehouse = (curr_warehouse, dist)

        if best_warehouse[0] != -1:
            return best_warehouse[0], qty
        # No warehouse found, so we try to find one with less qty.
        qty -= 1

        if qty == 0:
            raise Exception("No warehouse with enough stock")

    return best_warehouse[0], qty


def find_closest_cluster_to_obj(challenge: Map, obj, available_clusters: list):
    """
    Return the closest cluster to an object [Cluster | Warehouse]
    """
    best_cluster = (-1, -1)
    for id_cluster, cluster in available_clusters.items():
        current_dist = challenge.calc_dist(obj, cluster.orders[0])
        if current_dist <= best_cluster[1] or best_cluster[1] == -1:
            best_cluster = (id_cluster, current_dist)

    return best_cluster[0]


def qty_drone_can_load(challenge: Map, product_type: int, order_index: int):
    """
    Return the max amount of product a drone can take for a specific
    order product_type assuming that the drone is empty
    """
    current_order = challenge.orders[order_index]
    qty_wanted = current_order.products_qty[product_type]
    product_type_weight = challenge.product_weights[product_type]
    drone_max_payload = challenge.max_payload

    return min(drone_max_payload // product_type_weight, qty_wanted)


def current_payload_drone(challenge: Map, drone: Drone) -> int:
    """
    Return current payload for a specific drone
    """
    product_weights = challenge.product_weights
    current_load = sum(
        [qty * product_weights[ind] for ind, qty in enumerate(drone.stock)]
    )

    return current_load


def max_qty_allowed_to_load(
        challenge: Map,
        drone: Drone,
        product_type: int
) -> int:
    """
    Return max qty that a drone can take for a
    specifc product and check the current drone payload
    """
    product_weight = challenge.product_weights[product_type]
    current_payload = current_payload_drone(challenge, drone)
    max_payload = challenge.max_payload
    allowed_payload = max_payload - current_payload

    return allowed_payload // product_weight


def makeCommand(
        action: str,
        solution: list,
        drone_id: int,
        dest_id: int,
        product_type: int,
        qty: int,
) -> None:
    """
    Take an action either "L" or "D" and write a
    string to append into the list solution
    """
    solution.append(
        str(drone_id)
        + " "
        + str(action)
        + " "
        + str(dest_id)
        + " "
        + str(product_type)
        + " "
        + str(qty)
    )


def makeCommands(
        solution: list,
        queue_load: list,
        queue_deliver: list
):
    # This method is called when we need to unqueue
    # so we write all load actions first then
    # we write all their deliver actions
    # Note : We though it would improve our score but it dont.
    # Still it generate stylish solutions :D
    for load_action in queue_load:
        makeCommand(
            "L",
            solution,
            load_action[0],
            load_action[1],
            load_action[2],
            load_action[3]
        )

    for deliver_action in queue_deliver:
        makeCommand(
            "D",
            solution,
            deliver_action[0],
            deliver_action[1],
            deliver_action[2],
            deliver_action[3],
        )


def sort_objects_by_distance_from_obj(
        challenge: Map,
        obj,
        objects_list_to_sort: list,
        ideal_cluster_size=1,
):
    """
    Take a challenge, an object and a list of other objects.
    Sort the list by closest to obj position.
    and return it.
    """
    sorted_list = []

    for current_obj in objects_list_to_sort:
        calc_dist = challenge.calc_dist(obj, current_obj)
        sorted_list.append((calc_dist, current_obj))

    # obj[0] corresponding to dist
    sorted_list = sorted(sorted_list, key=lambda obj: obj[0])
    sorted_list = [curr_obj[1] for curr_obj in sorted_list]

    if ideal_cluster_size > 1:
        sorted_list = sorted_list[0: ideal_cluster_size - 1]

    return sorted_list


def calc_total_weight_order(challenge: Map, order: Order) -> int:
    """
    Calc the total weight of an order
    """
    weights = challenge.product_weights
    total = 0

    for product_type, nb_prod in enumerate(order.products_qty):
        total += weights[product_type] * nb_prod

    return total


def create_clusters(
        challenge: Map,
        orders: list,
        weightcoeff: float,
        distcoeff: float,
        ideal_cluster_size: int
):
    """
    We create all the clusters for a Map
    """
    clustered_orders = []
    clusters = {}

    for current_order in orders:
        # if order not clustered
        if current_order not in clustered_orders:

            # We create a new cluster
            cluster_id = len(clusters)
            clusters[cluster_id] = Cluster(cluster_id, weightcoeff, distcoeff)
            clusters[cluster_id].append_orders(current_order)
            # by default the order is set in the cluster

            # We add the order to the clustered orders
            clustered_orders.append(current_order)

            # We fetch the available orders
            available_orders = [
                order for order in orders if order not in clustered_orders]
            # if there is not enough orders to make a cluster
            if (len(available_orders) < ideal_cluster_size):
                # We add all the remaining orders to the
                # current cluster without restrictions
                clusters[cluster_id].append_orders(available_orders)
                clustered_orders.extend(available_orders)

            # We make clusters with ideal size using the nearest orders
            else:
                # we fetch the nearest orders
                nearest_orders = sort_objects_by_distance_from_obj(
                    challenge,
                    current_order,
                    available_orders,
                    ideal_cluster_size
                )
                # We add the nearest orders to the cluster
                clusters[cluster_id].append_orders(nearest_orders)
                clustered_orders.extend(nearest_orders)

    return clusters


def sort_clusters_by_distance_from_cluster(
        challenge: Map,
        cluster: Cluster,
        clusters_to_sort: list[Cluster],
) -> list[Cluster]:
    """
    Take a challenge, a cluster and a list of other clusters.
    Sort the list by closest to cluster position.
    And return the list
    """
    sorted_list = []

    for id_cluster, current_cluster in clusters_to_sort.items():
        calc_dist = challenge.calc_dist(cluster,
                                        current_cluster)
        sorted_list.append((calc_dist, id_cluster))

    sorted_list = sorted(sorted_list, key=lambda x: x[0])
    sorted_list = [curr_cluster[1] for curr_cluster in sorted_list]

    return sorted_list


def sort_orders_by_weight(orders: list[Order]) -> list[Order]:
    """
    Sort orders by weight
    and return the list
    """
    sorted_orders = []
    for order in orders:
        sorted_orders.append((order, order.total_weight))

    sorted_orders = sorted(sorted_orders, key=lambda x: x[1])
    sorted_orders = [order[0] for order in sorted_orders]

    return sorted_orders


def rank_orders_by_weight(challenge: Map, orders: list[Order]) -> list[Order]:
    """
    Rank orders by weight and return the sorted list.
    """
    # We calculate the total weight of each order
    for order in orders:
        weight_order = calc_total_weight_order(challenge, order)
        order.total_weight = weight_order

    # We sort the orders by weight
    orders = sort_orders_by_weight(orders)

    # We calculate the ranking weight for each order (by position in the list)
    for weight_ind, order in enumerate(orders):
        order.weight_ranking = (len(orders) - weight_ind) / len(orders)

    return orders


def update_ranking_score_clusters(
        challenge: Map,
        tmp_cluster: Cluster,
        clusters: Cluster
) -> list[Cluster]:
    """
    We update the distance ranking to update the overall ranking score_ranking
    of every single cluster.
    """
    # Ranking by distance from the cluster
    calc_clusters_by_dist = sort_clusters_by_distance_from_cluster(
        challenge, tmp_cluster, clusters)

    # Updating the ranking
    for ind_dist, id_cluster in enumerate(calc_clusters_by_dist):
        cluster = clusters[id_cluster]
        cluster.calc_dist_ranking(ind_dist, len(clusters))

    return clusters


def find_best_cluster(clusters: list[Cluster]) -> int:
    """
    Find the best cluster by ranking
    """
    return max(clusters.values(), key=lambda c: c.score_ranking).cluster_id


# We empty the drones and add commands to the solution
def deliver_drone_and_emptying(gameM: Map,
                               commendL: list[tuple[int, int, int, int]],
                               commendD: list[tuple[int, int, int, int]],
                               solution: list):
    # set of drones to remove from the order
    for o in gameM.orders:
        for d in o.drones:
            for prodT, prodQTY in enumerate(d.stock):
                # if there is still product of this type in the drone
                if prodQTY > 0:
                    # We add the delivery command to the delivery list
                    commendD.append((d.index, o.index, prodT, prodQTY))
                    # the product is removed from the order
                    o.products_qty[prodT] -= prodQTY
                    # the product is removed from the drone
                    d.stock[prodT] -= prodQTY
                    d.totalLoad -= gameM.product_weights[prodT] * prodQTY
            # we remove the drones from the order
            o.drones.remove(d)
    # we add the commands to the solution
    for c in commendL:
        makeCommand("L", solution, *c)
    commendL.clear()
    for c in commendD:
        makeCommand("D", solution, *c)
    commendD.clear()
