"""
Data exploration
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import seaborn as sns
from scipy.stats import spearmanr, zscore
from scipy.linalg import sqrtm
from cca_zoo import wrappers

from nkicap import load_data


DATA = "data/enhanced_nki.tsv"


def plot_demo(datapath, basepath="results/descriptive"):
    """check demographic"""
    dataset = load_data(datapath=datapath)
    plt.figure()
    sns.histplot(data=dataset, x="age", hue="sex", multiple="stack")
    plt.title("Demographics")
    plt.savefig(f"{basepath}/demographic.png", dpi=300)


def plot_capcorr(datapath, basepath="results/descriptive/cap_correlation"):
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


def plot_corr(datapath, basepath="results/descriptive"):
    dataset = load_data(datapath=datapath)
    pearsons = dataset.iloc[:, 4:].corr().iloc[-16:, :-16]
    sc = spearmanr(dataset.iloc[:, 4:])
    spearman = pd.DataFrame(
        sc[0][-16:, :-16], index=pearsons.index, columns=pearsons.columns
    )
    plt.figure()
    sns.heatmap(pearsons, center=0, annot=False, square=True, linewidths=0.02, vmax=0.15, vmin=-0.15)
    plt.title("pearsons r")
    plt.tight_layout()
    plt.savefig(f"{basepath}/pearsonscorrelation.png", dpi=300)

    plt.figure()
    sns.heatmap(spearman, center=0, annot=False, square=True, linewidths=0.02, vmax=0.15, vmin=-0.15)
    plt.title("spearmans r")
    plt.tight_layout()
    plt.savefig(f"{basepath}/spearmanscorrelation.png", dpi=300)


def _cca(X, Y):
    ux, sx, vx = np.linalg.svd(X, 0)
    uy, sy, vy = np.linalg.svd(Y, 0)
    u, s, v = np.linalg.svd(ux.T.dot(uy), 0)
    a = (vx.T).dot(u)
    b = (vy.T).dot(v.T)
    return a, b, s


def plot_cca_weight(a, index, title):
    # plotting
    w = pd.DataFrame(a, index=index, columns=range(1, 9))
    sns.heatmap(w, square=True, center=0)
    plt.title(title)
    plt.xlabel("Canoncial mode")


def plot_cca_score(U, V, s):
    plt.figure(figsize=(9, 6))
    N = len(s)
    for i in range(N):
        plt.subplot(221 + i)
        plt.scatter(
            np.array(U[:, i]).reshape(710),
            np.array(V[:, i]).reshape(710),
            marker="o",
            c="b",
            s=25,
        )
        plt.xlabel("Canonical variate of mriq")
        plt.ylabel("Canonical variate of cap score")
        plt.title("Mode %i (corr = %.2f)" % (i + 1, s[i]))
        plt.xticks(())
        plt.yticks(())


def plot_cca(datapath, basepath="results/descriptive"):
    mriq = load_data(keyword="mriq_", datapath=datapath).apply(zscore)
    occ = load_data(keyword="occ", datapath=datapath).apply(zscore)
    dur = load_data(keyword="dur", datapath=datapath).apply(zscore)
    mriq_index = pd.read_csv("data/mriq_labels.tsv", index_col=0, sep="\t").values
    mriq_index = np.squeeze(mriq_index).tolist()

    cca_w_cap = []
    cca_w_mriq = []
    for cap, name in zip([occ, dur], ["occ", "dur"]):
        w_mriq, w_cap, s = _cca(X=mriq.values, Y=cap.values)
        cca_w_cap.append(w_cap[:, 0])
        cca_w_mriq.append(w_mriq[:, 0])

        plt.figure()
        plt.plot(100 * s ** 2 / sum(s ** 2), "-o")
        plt.title(f"CCA mriq x {name} variance expalined")
        plt.xlabel("Canonical mode")
        plt.ylabel("%")
        plt.savefig(f"{basepath}/cca_varexp_mriq-{name}.png", dpi=300)
        plt.close()

        plt.figure(figsize=(13, 7))
        plot_cca_weight(w_mriq, mriq_index, "mriq")
        plt.savefig(f"{basepath}/cca_weight_{name}-mriq.png", dpi=300)
        plt.tight_layout()
        plt.close()

        plt.figure()
        plot_cca_weight(w_cap, [f"{name}-{i + 1}" for i in range(8)], name)
        plt.savefig(f"{basepath}/cca_weight_{name}-cap.png", dpi=300)
        plt.close()

        plot_cca_score(
            mriq.values.dot(w_mriq[:, 0:4]),
            cap.values.dot(w_cap[:, 0:4]),
            s[0:4],
        )
        plt.savefig(f"{basepath}/cca_score_{name}.png", dpi=300)
        plt.close()


if __name__ == "__main__":
    plot_capcorr(DATA)
    plot_demo(DATA)
    plot_corr(DATA)
    plot_cca(DATA)
