"""
Data exploration
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats.stats import pearsonr
import seaborn as sns
from scipy.stats import spearmanr, zscore

from nkicap import Data


DATA = "data/enhanced_nki.tsv"


def plot_demo(data, basepath="results/descriptive"):
    """check demographic"""
    dataset = data.load()
    plt.figure()
    sns.histplot(data=dataset, x="age", hue="sex", multiple="stack")
    plt.title("Demographics")
    plt.savefig(f"{basepath}/demographic.png", dpi=300)


def plot_corr(data, basepath="results/descriptive"):
    cap = data.load("cap")
    mriq = data.load("mriq_")
    dataset = pd.concat([mriq, cap], axis=1)

    pearsons = dataset.corr().iloc[-16:, :-16]
    mriq_labels = mriq.columns.tolist()
    sc = spearmanr(dataset)
    spearman = pd.DataFrame(
        sc[0][-16:, :-16], index=pearsons.index, columns=mriq_labels
    )
    plt.figure(figsize=(13, 7))
    sns.heatmap(
        pearsons.T,
        center=0,
        annot=False,
        square=True,
        linewidths=0.02,
        vmax=0.15,
        vmin=-0.15,
    )
    plt.title("pearsons r")
    plt.tight_layout()
    plt.savefig(f"{basepath}/pearsonscorrelation.png", dpi=300)

    plt.figure(figsize=(13, 7))
    sns.heatmap(
        spearman.T,
        center=0,
        annot=False,
        square=True,
        linewidths=0.02,
        vmax=0.15,
        vmin=-0.15,
    )
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


def plot_cca_cap(data, basepath="results/descriptive"):
    occ = data.load("occ").apply(zscore)
    dur = data.load("dur").apply(zscore)

    w_occ, w_dur, s = _cca(X=occ.values, Y=dur.values)

    plt.figure()
    plt.plot(100 * s ** 2 / sum(s ** 2), "-o")
    plt.title(f"CCA CAP occurence x duration variance expalined")
    plt.xlabel("Canonical mode")
    plt.ylabel("%")
    plt.savefig(f"{basepath}/cca_varexp_occ-dur.png", dpi=300)
    plt.close()

    plt.figure(figsize=(13, 7))
    plot_cca_weight(w_occ, [f"occ-{i + 1}" for i in range(8)], "occ")
    plt.savefig(f"{basepath}/cca_weight_cap-occ.png", dpi=300)
    plt.tight_layout()
    plt.close()

    plt.figure()
    plot_cca_weight(w_dur, [f"dur-{i + 1}" for i in range(8)], "dur")
    plt.savefig(f"{basepath}/cca_weight_cap-dur.png", dpi=300)
    plt.close()

    plot_cca_score(
        occ.values.dot(w_occ[:, 0:4]),
        dur.values.dot(w_dur[:, 0:4]),
        s[0:4],
    )
    plt.savefig(f"{basepath}/cca_score_cap.png", dpi=300)
    plt.close()

    for i in range(8):
        print(pearsonr(w_occ[:, i], w_dur[:, i]))
        print(pearsonr(w_occ[:, i], w_dur[:, i]))


def plot_cca(data, basepath="results/descriptive"):
    occ = data.load("occ").apply(zscore)
    dur = data.load("dur").apply(zscore)
    mriq = data.load("mriq_").apply(zscore)
    mriq_labels = mriq.columns.tolist()

    cca_w_cap = []
    cca_w_mriq = []
    for cap, name in zip([occ, dur], ["occ", "dur"]):
        w_mriq, w_cap, s = _cca(X=mriq.values, Y=cap.values)
        cca_w_cap.append(w_cap)
        cca_w_mriq.append(w_mriq)

        plt.figure()
        plt.plot(100 * s ** 2 / sum(s ** 2), "-o")
        plt.title(f"CCA mriq x {name} variance expalined")
        plt.xlabel("Canonical mode")
        plt.ylabel("%")
        plt.savefig(f"{basepath}/cca_varexp_mriq-{name}.png", dpi=300)
        plt.close()

        plt.figure(figsize=(13, 7))
        plot_cca_weight(w_mriq, mriq_labels, "mriq")
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

    for i in range(8):
        print(pearsonr(cca_w_cap[0][:, i], cca_w_cap[1][:, i]))
        print(pearsonr(cca_w_mriq[0][:, i], cca_w_mriq[1][:, i]))


if __name__ == "__main__":
    import os

    basepath = "results/descriptive-drop"
    mriq_drop = ["mriq_19", "mriq_22"]
    # mriq_drop = None
    os.makedirs(basepath, exist_ok=True)

    data = Data(
        datapath=DATA,
        mriq_labeltype="summary",
        mriq_drop=mriq_drop,
    )
    plot_demo(data, basepath)
    plot_corr(data, basepath)
    plot_cca(data, basepath)
    plot_cca_cap(data, basepath)
