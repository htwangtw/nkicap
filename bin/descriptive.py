"""
Data exploration
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr, zscore
from scipy.linalg import sqrtm
from cca_zoo import wrappers

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


def _cca(X, Y):
    ux, sx, vx = np.linalg.svd(X, 0)
    uy, sy, vy = np.linalg.svd(Y, 0)
    u, s, v = np.linalg.svd(ux.T.dot(uy), 0)
    a = (vx.T).dot(u)
    b = (vy.T).dot(v.T)
    return a, b, s

def plot_cca(a):
    # plotting
    plt.figure()
    sns.heatmap(a, square=True, center=0)

def plot_cca_score(U, V, s):
    plt.figure(figsize=(9, 6))
    N = len(s)
    for i in range(N):
        plt.subplot(221 + i)
        plt.scatter(np.array(U[:, i]).reshape(710),
                    np.array(V[:, i]).reshape(710),
                    marker="o", c="b", s=25)
        plt.xlabel("Canonical variate of X")
        plt.ylabel("Canonical variate of Y")
        plt.title('Mode %i (corr = %.2f)' %(i + 1, s[i]))
        plt.xticks(())
        plt.yticks(())


def plot_corr(datapath="data/enhanced_nki.tsv", basepath="results/descriptive"):
    mriq = load_data(keyword="mriq_", datapath=datapath).apply(zscore)
    occ = load_data(keyword="occ", datapath=datapath).apply(zscore)
    dur = load_data(keyword="dur", datapath=datapath).apply(zscore)

    cca_w_cap = []
    cca_w_mriq = []
    for cap, name in zip([occ, dur], ["occ", "dur"]):
        w_mriq, w_cap, s = _cca(X=mriq.values, Y=cap.values)
        cca_w_cap.append(w_cap[:, 0])
        cca_w_mriq.append(w_mriq[:, 0])
        print(name)
        print(s**2 /sum(s**2))

        plot_cca(w_mriq[:, 0: 4])
        plt.savefig(f"{basepath}/cca_score_{name}-mriq.png", dpi=300)
        plt.close()

        plot_cca(w_cap[:, 0: 4])
        plt.savefig(f"{basepath}/cca_score_{name}-cap.png", dpi=300)
        plt.close()

        plot_cca_score(mriq.values.dot(w_mriq[:, 0: 4]), cap.values.dot(w_cap[:, 0: 4]), s[0: 4])
        plt.savefig(f"{basepath}/cca_weight_{name}.png", dpi=300)
        plt.close()



if __name__ == "__main__":
    # plot_capcorr()
    # plot_demo()
    plot_corr()
