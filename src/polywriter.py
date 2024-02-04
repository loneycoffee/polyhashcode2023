from polysolvers import (
    naive_approach_loic,
    naive_approach_theo,
    naive_approach_amedeo,
)
import sys


def Writer(challenge: str, method: str, output_name: str = None) -> None:
    if method == "loic":
        solution = naive_approach_loic(challenge)
    elif method == "theo":
        solution = naive_approach_theo(challenge)
    elif method == "amedeo":
        solution = naive_approach_amedeo(challenge)
    else:
        print("This algorithm doesn't exist")
        return

    # basename if no output_name specified take the
    # challenge name and add .out at the end.
    if output_name is None:
        output_name = (
            "solutions/" + "solutions_" + str(method) + "/"
            + str(str(challenge.split("/")[-1]).split(".")[0]) + ".out"
        )

    with open(output_name, "w") as f:
        # Write the number of line at the begining.
        f.write(str(len(solution)) + "\n")
        for line in solution:
            f.write(line + "\n")
