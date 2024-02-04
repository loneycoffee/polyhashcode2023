import os
import sys

from polywriter import Writer

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "usage: python polyhash.py theo|loic|amedeo "
            + "[challenges/map.in] [solutions/map.out]"
        )
    else:
        print("Generating solutions using : " + str(sys.argv[1]) + "...")

        if len(sys.argv) >= 4:
            Writer(sys.argv[2], sys.argv[1], sys.argv[3])
        else:
            if len(sys.argv) == 3:
                Writer(sys.argv[2], sys.argv[1])
            else:
                for file in os.listdir("challenges/"):
                    print("Generating solution for " + str(file) + "...")
                    Writer("challenges/" + str(file), sys.argv[1])
