"""Data exploration"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from scipy.stats import spearmanr, zscore
from scipy.stats.stats import pearsonr

from nkicap import Data

DATA = "data/enhanced_nki.tsv"


def plot_demo(data, basepath="results/descriptive"):
    """Check demographic."""
    dataset = data.load()
    plt.figure()
    sns.histplot(data=dataset, x="age", hue="sex", multiple="stack")
    plt.title("Demographics")
    plt.savefig(f"{basepath}/demographic.png", dpi=300)


def plot_occ_dur(data, basepath="results/descriptive"):
    """Sanity check on the CAP occurence and duration."""
    cap = data.load("cap")
    pearsons = cap.corr().iloc[8:, :8]
    plt.figure(figsize=(7, 5))
    sns.heatmap(
        pearsons,
        center=0,
        annot=True,
        square=True,
        linewidths=0.02,
        vmax=1,
        vmin=-1,
    )
    plt.title("CAP correlations (sainity check)")
    plt.tight_layout()
    plt.savefig(f"{basepath}/occ_dur.png", dpi=300)


def plot_corr(cap, mriq, prefix, basepath="results/descriptive"):
    """Simple correlation between all CAP features and MRIQ."""
    dataset = pd.concat([mriq, cap], axis=1)
    mriq_labels = mriq.columns.tolist()
    corr_mat_size = cap.shape[1]

    pearsons = dataset.corr().iloc[-corr_mat_size:, :-corr_mat_size]
    corr_mat_mriq(pearsons.T, "pearsons r", f"{basepath}/{prefix}_pearsons.png")
    sc = spearmanr(dataset)
    spearman = pd.DataFrame(
        sc[0][-corr_mat_size:, :-corr_mat_size],
        index=pearsons.index,
        columns=mriq_labels,
    )
    corr_mat_mriq(spearman.T, "spearman r", f"{basepath}/{prefix}_spearmans.png")


def corr_mat_mriq(mat, title, path):
    """Plot the simple correlation and enough space to show the full questions."""
    plt.figure(figsize=(13, 7))
    sns.heatmap(
        mat,
        center=0,
        annot=False,
        square=True,
        linewidths=0.02,
        vmax=0.15,
        vmin=-0.15,
    )
    plt.title(title)
    plt.tight_layout()
    plt.savefig(path, dpi=300)


def cap_pairs(data):
    """Calculate differences of CAP pairs."""
    cap = data.load("cap")
    diffs = pd.DataFrame()
    for i in range(4):
        first = 2 * i + 1
        second = first + 1
        occ_diff = cap[f"occ_cap_0{first}"] - cap[f"occ_cap_0{second}"]
        occ_diff.name = f"occ_cap_0{first}_0{second}"
        dur_diff = cap[f"dur_cap_0{first}"] - cap[f"dur_cap_0{second}"]
        dur_diff.name = f"dur_cap_0{first}_0{second}"
        diffs = pd.concat([diffs, occ_diff, dur_diff], axis=1)
        diffs.index.name = "participant_id"
    return diffs.reindex(sorted(diffs.columns), axis=1)


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
    plt.title("CCA CAP occurence x duration variance expalined")
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

    basepath = "results/descriptive"
    os.makedirs(basepath, exist_ok=True)

    mriq_drop = ["mriq_19", "mriq_22"]
    data = Data(
        datapath=DATA,
        mriq_labeltype="full",
        mriq_drop=None,
    )
    diff = cap_pairs(data)
    cap = data.load("cap")
    mriq = data.load("mriq_")
    plot_occ_dur(data, basepath)
    plot_demo(data, basepath)
    plot_corr(cap, mriq, "cap-raw", basepath)
    plot_corr(diff, mriq, "cap-pairs", basepath)
    # plot_cca(data, basepath)
    # plot_cca_cap(data, basepath)
