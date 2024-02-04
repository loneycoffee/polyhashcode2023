from polywriter import Writer
import resource
import sys
import time
import os

"""
This module makes reports of our algorithms
performance both in time spent and memory used
"""


def bench(file: str, method: str):
    t1 = time.perf_counter()
    d1 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    Writer(str(file), str(method))
    t2 = time.perf_counter()
    d2 = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(str(file) + " : " + " " * (40 - len(str(file)))
          + str(round(t2 - t1, 3)) + " seconds")
    print(" " * (43) + str((d2 - d1) / 1000) + " MB")


def bench_all(method: str = None, challenge: str = None):
    challenge_to_bench = [
        "challenges/a_example.in",
        "challenges/b_busy_day.in",
        "challenges/c_redudancy.in",
        "challenges/d_mother_of_all_warehouses.in",
    ]

    algos_to_bench = [
        "theo",
        "loic",
        "amedeo",
    ]

    if method == "every" or method is None:
        for algo in algos_to_bench:
            print("===========")
            print("Using " + str(algo) + " algorithm...")
            if challenge == "every":
                for file in os.listdir("challenges/"):
                    bench("challenges/" + file, algo)
            elif challenge is None:
                for file in challenge_to_bench:
                    bench(file, algo)
            else:
                bench(challenge, algo)
        print("===========")
    else:
        print("===========")
        print("Using " + str(method) + " algorithm...")
        if challenge == "every":
            for file in os.listdir("challenges/"):
                bench("challenges/" + file, method)
        elif challenge is None:
            for file in challenge_to_bench:
                bench(file, method)
        else:
            bench(challenge, method)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(
            "usage: python polybench.py\
            every|theo|loic|amedeo [every|challenges/map.in]"
        )
    elif len(sys.argv) == 2:
        bench_all(sys.argv[1], None)
    elif len(sys.argv) >= 3:
        bench_all(sys.argv[1], sys.argv[2])
