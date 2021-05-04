"""Plot CAP maps in gradient space for presentations."""
from nkicap.gradient import cap_to_gradient
from nkicap.utils import get_project_path
import matplotlib.pyplot as plt
from pathlib import Path


gradient_space = cap_to_gradient(
    Path(get_project_path()) / "data/cap_gradient_space.tsv"
)

cap_color = {
    1: "yellowgreen",
    2: "forestgreen",
    3: "coral",
    4: "firebrick",
    5: "darkslategrey",
    6: "teal",
    7: "royalblue",
    8: "lightsteelblue",
}


def plot_caps(x_label, ylabel, cap_range):
    sub = gradient_space["participant_id"] != "group"
    scatter = []
    fig = plt.figure()
    for i in cap_range:
        mask = gradient_space["CAP"] == i
        plt.scatter(
            gradient_space[mask * sub][x_label],
            gradient_space[mask * sub][ylabel],
            alpha=0.2,
            color=cap_color[i],
        )

        g = plt.scatter(
            gradient_space[mask * ~sub][x_label],
            gradient_space[mask * ~sub][ylabel],
            marker="+",
            color=cap_color[i],
        )
        scatter.append(g)
    plt.xlabel(x_label)
    plt.ylabel(ylabel)
    plt.legend(scatter, [f"CAP {i}" for i in cap_range])
    return fig


if __name__ == "__main__":
    group_1 = plot_caps("Gradient 1", "Gradient 2", range(1, 5))
    group_2 = plot_caps("Gradient 1", "Gradient 3", range(5, 9))

    group_1.savefig("results/gradient_space_cap_1-4.png")
    group_2.savefig("results/gradient_space_cap_5-8.png")
