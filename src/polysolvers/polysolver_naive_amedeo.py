"""
Module de résolution du projet Poly#.
"""
from Objects import Map
from polyparser import parse_challenge
from utils.functs import (
    sort_objects_by_distance_from_obj,
    makeCommand,
    deliver_drone_and_emptying)


def naive_approach_amedeo(challenge):
    """
    Naive algorithm where we iterate over the orders,
    sorted by weight to start with the fastest to finish.
    The nearest Warehouses are calculated. Each product type is iterated over.
    Then the current drone is filled, and if it's full, the next one is taken.
    Once all the drones are full, we empty them.
    """
    solution = []
    gameM: Map = parse_challenge(challenge)

    # We sort the orders by weight
    oWeightSort = sorted(gameM.orders, key=lambda x: sum(x.products_qty))

    # Index of the current drone
    dPointer = 0
    # Current drone
    dCurent = gameM.drones[dPointer]

    # we sort the warehouses by distance from the first warehouse
    wDistSort = sort_objects_by_distance_from_obj(
        gameM, gameM.warehouses[0], gameM.warehouses)

    # list of load commands
    commendL: list[tuple[int, int, int, int]] = []
    # list of deliver commands
    commendD: list[tuple[int, int, int, int]] = []

    # For each order of the sorted order list
    for oIndex, oCurent in enumerate(oWeightSort):
        # Index of the current warehouse
        wPointer = 0
        # current warehouse
        wCurent = wDistSort[wPointer]
        # for each product type in the order
        for prodT, _ in enumerate(oCurent.products_qty):
            # While there is still products to send
            while oCurent.products_qty[prodT] > 0:
                # If there is no more of this product in the warehouse
                if wCurent.stock[prodT] <= 0:
                    # We go to the next warehouse
                    wPointer = (wPointer + 1) % len(wDistSort)
                    wCurent = wDistSort[wPointer]
                    continue

                # Calcul the quantity of product to send
                qtyL = min(
                    gameM.max_payload // gameM.product_weights[prodT],
                    wCurent.stock[prodT],
                    oCurent.products_qty[prodT])

                # if the drone is full if we add more of this product
                while dCurent.totalLoad + \
                        (gameM.product_weights[prodT] * qtyL) \
                        > gameM.max_payload:
                    # if all drones are full
                    if (dPointer + 1) % gameM.nb_drones == 0:
                        # We empty the drones and add write
                        # the commands to the solution
                        (deliver_drone_and_emptying
                         (gameM, commendL, commendD, solution))
                    # We go to the next drone
                    dPointer = (dPointer + 1) % gameM.nb_drones
                    dCurent = gameM.drones[dPointer]

                # add the load command to the load list
                commendL.append((dCurent.index, wCurent.index, prodT, qtyL))

                # The object is removed from the warehouse
                wCurent.stock[prodT] -= qtyL

                # The object is added to the drone
                dCurent.stock[prodT] += qtyL
                dCurent.totalLoad += gameM.product_weights[prodT] * qtyL

                # The drone is added to the order if is not already in
                if dCurent not in oCurent.drones:
                    oCurent.drones.append(dCurent)
                oCurent.products_qty[prodT] -= qtyL
    deliver_drone_and_emptying(gameM, commendL, commendD, solution)
    return solution
