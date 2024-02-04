import sys

from polyparser import parse_challenge


def printr(txt):
    return ("\033[91m" + str(txt) + "\033[00m")


def printg(txt):
    return ("\033[92m" + str(txt) + "\033[00m")


def map_visualizer_init(challenge):
    challenge = parse_challenge(challenge)

    number_needed = max(len(str(len(challenge.warehouses))),
                        len(str(len(challenge.orders)))) - 1

    print("X = rien")
    print(printg("X") + " = order n°X")
    print(printr("X") + " = warehouse n°X")
    print("Les drones commencent toujours sur la warehouse n°0")

    grid = []  # X = None , X in red = warehouse n°X, X in gree = order n°X
    for row in range(challenge.rows - 1):
        grid.append([])
        for col in range(challenge.cols):
            grid[row].append(("X", number_needed - 1))

    for warehouse_index in range(len(challenge.warehouses)):
        dest = challenge.warehouses[warehouse_index].position
        grid[dest[0]][dest[1]] = (printr(warehouse_index), warehouse_index)

    for order_index in range(len(challenge.orders)):
        dest = challenge.orders[order_index].position
        grid[dest[0]][dest[1]] = (printg(order_index), order_index)

    for row in grid:
        print("")
        print("|", end="")
        for item in row:
            print(item[0] + (str(" ")
                             * (number_needed - len(str(item[1])))), end="")

            print("|", end="")
    print("\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python polyvisualizer ../challenges/ma_map.in")
    else:
        map_visualizer_init(sys.argv[1])
