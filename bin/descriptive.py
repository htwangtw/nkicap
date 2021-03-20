"""
Data exploration
"""

import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr

from nkicap import load_data


def plot_demo(datapath="data/enhanced_nki.tsv", basepath="results/descriptive"):
    """check demographic"""
    dataset = load_data(datapath=datapath)
    plt.figure()
    sns.histplot(data=dataset, x="age", hue="sex", multiple="stack")
    plt.title("Demographics")
    plt.savefig(f"{basepath}/demographic.png", dpi=300)


def plot_capcorr(datapath="data/enhanced_nki.tsv", basepath="results/descriptive/cap_correlation"):
    # check the correlation between occurence and duration
    cap = load_data(keyword="cap", datapath=datapath)
    plt.figure()
    sns.heatmap(
        cap.corr().iloc[:8, 8:], center=0, annot=True, square=True, linewidths=0.02
    )
    plt.title("CAP correlation")
    plt.tight_layout()
    plt.savefig(f"{basepath}_heat.png", dpi=300)

    plt.figure()
    sns.pairplot(
        cap,
        x_vars=[c for c in cap.columns.tolist() if "dur" in c],
        y_vars=[c for c in cap.columns.tolist() if "occ" in c],
    )
    plt.tight_layout()
    plt.savefig(f"{basepath}_scatter.png", dpi=300)


def plot_corr(datapath="data/enhanced_nki.tsv", basepath="results/descriptive"):
    dataset = load_data(datapath=datapath)
    plt.figure()
    sns.heatmap(
        dataset.corr().iloc[-16:, 2:-16],
        center=0,
        annot=False,
        square=True,
        linewidths=0.02,
    )
    plt.title("correlation")
    plt.tight_layout()
    plt.savefig(f"{basepath}/pearsonscorrelation.png", dpi=300)

    sc = spearmanr(dataset)
    plt.figure()
    sns.heatmap(sc[0][-16:, 2:-16], center=0, annot=False, square=True, linewidths=0.02)
    plt.title("correlation")
    plt.tight_layout()
    plt.savefig(f"{basepath}/spearmanscorrelation.png", dpi=300)


if __name__ == "__main__":
    plot_capcorr()
    plot_demo()
    plot_corr()
