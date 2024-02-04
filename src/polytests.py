from Objects import Map, Drone, Warehouse, Cluster, Order
from polyparser import parse_challenge
from polywriter import Writer
from polysolvers import (
    naive_approach_loic,
    naive_approach_theo,
    naive_approach_amedeo
)
from utils.functs import (
    find_closest_warehouse,
    find_closest_cluster_to_obj,
    qty_drone_can_load,
    current_payload_drone,
    create_clusters,
    max_qty_allowed_to_load,
    sort_objects_by_distance_from_obj,
    calc_total_weight_order,
    sort_clusters_by_distance_from_cluster,
    sort_orders_by_weight,
    rank_orders_by_weight,
    update_ranking_score_clusters,
    find_best_cluster,
    deliver_drone_and_emptying
)


def printr(txt):
    print("\033[91m{}\033[00m".format(txt))


def printg(txt):
    print("\033[92m{}\033[00m".format(txt))


def test_drone():
    d0 = Drone(0, (0, 0), [1, 1, 1])
    assert Map.calc_dist(d0, d0) == 0

    d1 = Drone(1, (2, 2), [1, 1, 1])
    d2 = Drone(0, (0, 0), [1, 1, 1])
    assert Map.calc_dist(d1, d2) == 3

    d1 = Drone(0, (0, 0), [1, 1, 1])
    d2 = Drone(0, (0, 3), [1, 1, 1])
    assert Map.calc_dist(d1, d2) == 3

    printg("Drone class tests PASSED")


def test_warehouse():
    w0 = Warehouse(0, (0, 0), [1, 1, 1])
    assert not w0.is_empty()

    w1 = Warehouse(1, (0, 0), [0, 0, 0])
    assert w1.is_empty()

    printg("Warehouse class tests PASSED")


def test_order():
    o0 = Order(0, (0, 0), 3, [1, 1, 1])
    assert not o0.check_full_filled()

    o1 = Order(1, (0, 0), 3, [1, 1, 1])
    assert not o1.check_full_filled()

    printg("Order class tests PASSED")


def test_cluster():
    m = parse_challenge("challenges/a_example.in")
    c1 = Cluster(0, 0.1, 0.9)
    assert c1.position is None

    # Adding a single order
    m.orders[0].weight_ranking = 0.2
    c1.append_orders(m.orders[0])
    assert not c1.are_orders_full_filled()
    assert c1.position == c1.orders[0].position
    assert c1.get_first_order() == c1.orders[0]

    # Adding multiple orders
    m.orders[1].weight_ranking = 0.1
    m.orders[2].weight_ranking = 0.3
    orders = [m.orders[1], m.orders[2]]
    c1.append_orders(orders)
    assert c1.get_first_order() == c1.orders[0]

    assert round(c1.weight_ranking, 1) == 0.2

    c1.del_order_full_filled(c1.orders[0])
    assert len(c1.orders) == 2
    assert c1.get_first_order() == m.orders[1]

    # Testing weight ranking calc
    c1.weight_ranking = 0.9
    c1.dist_ranking = 0.24
    c1.calc_score_ranking()
    assert c1.score_ranking == 0.306

    c1.calc_dist_ranking(0, 3)
    assert c1.dist_ranking == 1.0

    c2 = c1.copy_cluster()
    assert c1.orders[0].total_weight == c2.orders[0].total_weight
    assert c1.dist_ranking == c2.dist_ranking
    assert c1.position == c2.position

    c2.del_order_full_filled(c2.orders[0])
    c2.del_order_full_filled(c2.orders[0])
    assert c2.are_orders_full_filled()

    printg('Cluster class tests PASSED')


def test_parse_challenge():
    m = parse_challenge("challenges/a_example.in")
    assert m.rows == 100
    assert m.cols == 100
    assert m.nb_drones == 3
    assert m.nb_turns == 50
    assert m.max_payload == 500
    assert m.max_payload == 500
    assert m.product_weights == [100, 5, 450]
    assert m.warehouses[0].position == (0, 0)
    assert m.warehouses[0].stock == [5, 1, 0]
    assert m.warehouses[1].position == (5, 5)
    assert m.warehouses[1].stock == [0, 10, 2]
    assert m.orders[0].position == (1, 1)
    assert m.orders[0].nb_products == 2
    assert m.orders[0].products_qty == [1, 0, 1]
    assert m.orders[1].position == (3, 3)
    assert m.orders[1].nb_products == 1
    assert m.orders[1].products_qty == [1, 0, 0]
    assert m.orders[1].nb_products == 1
    assert m.orders[2].position == (5, 6)
    assert m.orders[2].nb_products == 1
    assert m.orders[2].products_qty == [0, 0, 1]
    assert len(m.drones) == m.nb_drones
    for i in range(m.nb_drones):
        assert m.drones[i].position == m.warehouses[0].position

    printg("-> Parser tests PASSED")


def test_find_closest_warehouse():
    m = parse_challenge("challenges/test_utils.in")
    # Using test_utils challenge, closest warehouse for product type 0 and
    # quantity 1 should be warehouse 0
    assert find_closest_warehouse(m, 0, 0, 1)[0].index == 0
    # closest warehouse for product type 2 and quantity 1 should be warehouse 1
    assert find_closest_warehouse(m, 0, 2, 1)[0].index == 1
    # closest warehouse for product type 1 and quantity 1 should be warehouse 0
    assert find_closest_warehouse(m, 0, 1, 1)[0].index == 0
    # closest warehouse for product type 0 and quantity 1 should be warehouse 0
    assert find_closest_warehouse(m, 0, 0, 5)[0].index == 0
    printg("find_closest_warehouse tests PASSED")


def test_find_closest_cluster_to_obj():
    m = parse_challenge("challenges/a_example.in")
    w0 = m.warehouses[0]
    clusters = create_clusters(m, m.orders, 0.1, 0.9, 2)
    assert find_closest_cluster_to_obj(
        m, w0, clusters) == clusters[0].cluster_id

    w1 = m.warehouses[1]
    assert find_closest_cluster_to_obj(
        m, w1, clusters) == clusters[1].cluster_id

    printg('find_closest_cluster_to_obj tests PASSED')


def test_current_payload_drone():
    m = parse_challenge("challenges/test_utils.in")
    drone = m.drones[0]
    drone.stock = [1, 0, 0]
    assert current_payload_drone(m, drone) == m.product_weights[0] * 1
    drone.stock = [0, 2, 0]
    assert current_payload_drone(m, drone) == m.product_weights[1] * 2
    drone.stock = [0, 0, 0]
    assert current_payload_drone(m, drone) == 0

    printg("current_payload_drone tests PASSED")


def test_qty_drone_can_load():
    m = parse_challenge("challenges/a_example.in")
    assert qty_drone_can_load(m, 0, 0) == 1
    assert qty_drone_can_load(m, 0, 2) == 0

    printg("qty_drone_can_load tests PASSED")


def test_max_qty_allowed_to_load():
    m = parse_challenge("challenges/a_example.in")
    d0 = m.drones[0]
    assert max_qty_allowed_to_load(m, d0, 0) == 5
    d0.stock[0] = 5
    assert max_qty_allowed_to_load(m, d0, 0) == 0

    printg("max_qty_allowed_to_load tests PASSED")


def test_sort_objects_by_distance_from_object():
    m = parse_challenge("challenges/a_example.in")
    orders = m.orders
    w0 = m.warehouses[0]
    w1 = m.warehouses[1]

    assert sort_objects_by_distance_from_obj(m, w0, orders) == orders
    assert sort_objects_by_distance_from_obj(m, w1, orders) == [
        orders[2], orders[1], orders[0]]

    printg("sort_objects_by_distance_from_obj tests PASSED")


def test_calc_total_weight_order():
    m = parse_challenge("challenges/a_example.in")
    o0 = m.orders[0]
    o1 = m.orders[1]
    o2 = m.orders[2]

    assert calc_total_weight_order(m, o0) == 550
    assert calc_total_weight_order(m, o1) == 100
    assert calc_total_weight_order(m, o2) == 450

    printg("calc_total_weight_order tests PASSED")


def test_create_clusters():
    m = parse_challenge("challenges/a_example.in")
    orders = m.orders
    clusters = create_clusters(m, orders, 0.9, 0.1, 2)
    c1 = Cluster(0, 0.9, 0.1)
    c1.append_orders([orders[0], orders[1]])

    c2 = Cluster(1, 0.9, 0.1)
    c2.append_orders(orders[2])

    assert len(clusters) == 2
    assert c1.orders == clusters[0].orders
    assert c2.orders == clusters[1].orders

    printg("create_clusters tests PASSED")


def test_sort_clusters_by_distance_from_cluster():
    m = parse_challenge("challenges/a_example.in")
    orders = m.orders
    clusters = create_clusters(m, orders, 0.9, 0.1, 2)

    assert sort_clusters_by_distance_from_cluster(
        m, clusters[0], clusters) == [clusters[0].cluster_id,
                                      clusters[1].cluster_id]

    printg("sort_clusters_by_distance_from_cluster tests PASSED")


def test_sort_orders_by_weight():
    m = parse_challenge("challenges/a_example.in")
    orders = m.orders

    for order in orders:
        weight_order = calc_total_weight_order(m, order)
        order.total_weight = weight_order

    orders = sort_orders_by_weight(orders)

    assert orders[0].index == 1
    assert orders[1].index == 2
    assert orders[2].index == 0

    printg("sort_orders_by_weight tests PASSED")


def test_rank_orders_by_weight():
    m = parse_challenge("challenges/a_example.in")
    orders = m.orders
    orders = rank_orders_by_weight(m, orders)

    assert orders[0].index == 1
    assert round(orders[0].weight_ranking, 2) == 1.00
    assert orders[1].index == 2
    assert round(orders[1].weight_ranking, 2) == 0.67
    assert orders[2].index == 0
    assert round(orders[2].weight_ranking, 2) == 0.33

    printg("rank_orders_by_weight tests PASSED")


def test_update_ranking_score_clusters():
    m = parse_challenge("challenges/a_example.in")
    orders = m.orders
    orders = rank_orders_by_weight(m, orders)
    clusters = create_clusters(m, orders, 0.9, 0.1, 2)
    tmp_cluster = clusters[0].copy_cluster()
    clusters = update_ranking_score_clusters(m, tmp_cluster, clusters)

    assert clusters[0].score_ranking == 0.7
    assert clusters[1].score_ranking == 0.65

    printg("test_update_ranking_score_clusters tests PASSED")


def test_find_best_cluster():
    m = parse_challenge("challenges/a_example.in")
    orders = m.orders
    orders = rank_orders_by_weight(m, orders)
    clusters = create_clusters(m, orders, 0.9, 0.1, 2)
    tmp_cluster = clusters[0].copy_cluster()
    clusters = update_ranking_score_clusters(m, tmp_cluster, clusters)
    best_cluster = find_best_cluster(clusters)

    assert best_cluster == clusters[0].cluster_id

    printg("test_find_best_cluster tests PASSED")

    def test_deliver_drone_and_emptying():
        m = parse_challenge("challenges/a_example.in")
        commendL = ["0 L 0 0 1"]
        commendD = ["0 D 1 0 1"]
        solution = []
        deliver_drone_and_emptying(m, commendL, commendD, solution)
        assert m.warehouses[0].stock == [4, 1, 0]
        assert m.drones[0].stock == [1, 0, 0]
        assert m.orders[0].products_qty == [0, 0, 1]
        assert solution == ["0 L 0 0 1", "0 D 1 0 1"]

        printg("test_deliver_drone_and_emptying tests PASSED")


def test_naive_loic():
    solution = naive_approach_loic("challenges/a_example.in")
    # Must use set to tests equity between 2 lists.
    assert set(solution) == set(
        [
            "0 L 0 0 1",
            "1 L 1 2 1",
            "0 D 0 0 1",
            "1 D 0 2 1",
            "2 L 0 0 1",
            "2 D 1 0 1",
            "0 L 1 2 1",
            "0 D 2 2 1",
        ]
    )

    printg("Solution naive loic tests PASSED")


def test_naive_theo():
    solution = naive_approach_theo("challenges/a_example.in")
    # Must use set to tests equity between 2 lists.
    assert set(solution) == set(
        [
            "1 L 0 0 1",
            "1 D 1 0 1",
            "1 L 0 0 1",
            "1 D 0 0 1",
            "1 L 1 2 1",
            "1 D 0 2 1",
            "2 L 1 2 1",
            "2 D 2 2 1"
        ]
    )

    printg("Solution naive theo tests PASSED")


def test_naive_amedeo():
    solution = naive_approach_amedeo("challenges/a_example.in")
    # Must use set to tests equity between 2 lists.
    assert set(solution) == set(
        [
            "0 L 0 0 1",
            "1 L 1 2 1",
            "2 L 0 0 1",
            "2 D 0 0 1",
            "0 D 1 0 1",
            "1 D 2 2 1",
            "0 L 1 2 1",
            "0 D 0 2 1"
        ]
    )

    printg("Solution naive amedeo tests PASSED")


def test_writer():
    # Testing if writer hasn't changed, if it has, you may want to update the
    # solutions stored in solutions_test to pass this test
    Writer("challenges/a_example.in", "loic")
    assert set(open("solutions/solutions_loic/a_example.out")) == set(
        open("solutions_test/a_example_loic.test")
    )

    Writer("challenges/b_busy_day.in", "loic")
    assert set(open("solutions/solutions_loic/b_busy_day.out")) == set(
        open("solutions_test/b_busy_day_loic.test")
    )
    printg("Writer tests PASSED for loic")

    Writer("challenges/a_example.in", "theo")
    assert set(open("solutions/solutions_theo/a_example.out")) == set(
        open("solutions_test/a_example_theo.test")
    )

    Writer("challenges/b_busy_day.in", "theo")
    assert set(open("solutions/solutions_theo/b_busy_day.out")) == set(
        open("solutions_test/b_busy_day_theo.test")
    )

    printg("Writer tests PASSED for theo")

    Writer("challenges/a_example.in", "amedeo")
    assert set(open("solutions/solutions_amedeo/a_example.out")) == set(
        open("solutions_test/a_example_amedeo.test")
    )

    Writer("challenges/b_busy_day.in", "amedeo")
    assert set(open("solutions/solutions_amedeo/b_busy_day.out")) == set(
        open("solutions_test/b_busy_day_amedeo.test")
    )

    printg("Writer tests PASSED for amedeo")

    printg("-> Writer tests COMPLETED")


if __name__ == "__main__":
    print('\nTesting parsing...')
    test_parse_challenge()

    print('\nTesting Objects...')
    test_drone()
    test_warehouse()
    test_order()
    test_cluster()
    printg('-> Objects tests COMPLETED')

    print('\nTesting utils.functs...')
    test_find_closest_warehouse()
    test_find_closest_cluster_to_obj()
    test_current_payload_drone()
    test_qty_drone_can_load()
    test_max_qty_allowed_to_load()
    test_sort_objects_by_distance_from_object()
    test_calc_total_weight_order()
    test_create_clusters()
    test_sort_clusters_by_distance_from_cluster()
    test_sort_orders_by_weight()
    test_rank_orders_by_weight()
    test_update_ranking_score_clusters()
    test_find_best_cluster()

    printg('-> utils.functs tests COMPLETED')

    print('\nTesting solutions for each approach')
    test_naive_loic()
    test_naive_theo()
    test_naive_amedeo()

    print('\nTesting Writer...')
    test_writer()
