import sys

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import statsmodels.formula.api as smf
from scipy.stats.stats import zscore
from statsmodels.multivariate.manova import MANOVA
from statsmodels.stats.multitest import multipletests

from nkicap import Data

DATA = "data/enhanced_nki.tsv"


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


def mmr_with_fig(endog, exog, dataset, basepath):
    manova = MANOVA(endog=endog, exog=exog)

    manova.mv_test().summary_frame.to_csv(f"{basepath}/multivariate_results.csv")
    results = manova.mv_test().results
    sig_key = []

    for key, (_, output) in zip(manova.mv_test().exog_names, results.items()):
        p_val = output["stat"]["Pr > F"][0]
        key = (" ").join(key.split("_"))
        if p_val < 0.05:
            sig_key.append((key, p_val))
        # partial eta square
        f_val = output["stat"]["F Value"][0]
        den_df = output["stat"]["Den DF"][0]
        num_df = output["stat"]["Num DF"][0]
        par_eta_sqr = num_df * f_val / (num_df * f_val + den_df)
        print("partical eta squared of {}: {}".format(key, par_eta_sqr))

    if not sig_key:
        sig_key.append(("None", "N/A"))

    df_coef = pd.DataFrame()
    df_pval = pd.DataFrame()
    iv_formula = " + ".join(exog.columns.tolist())
    for dv in manova.endog_names:
        univeriate = smf.ols(formula=f"{dv} ~ {iv_formula}", data=dataset).fit()
        print(univeriate.summary())
        p_adjust = multipletests(univeriate.pvalues, alpha=0.05, method="bonferroni")
        df_coef = df_coef.append(univeriate.params, ignore_index=True)
        df_p_adjust = pd.DataFrame(
            np.array([p_adjust[0], p_adjust[1]]).T,
            index=["Intercept"] + exog.columns.tolist(),
            columns=["Sig.", "p_adjusted"],
        )
        df_pval = df_pval.append(df_p_adjust.iloc[:, 1], ignore_index=True)
        print(df_p_adjust)
        print(
            "Bonferroni corrected alpha (0.05): {}\n".format(
                multipletests(univeriate.pvalues, alpha=0.05, method="bonferroni")[-1]
            )
        )

    df_coef.index = manova.endog_names
    df_pval.index = df_coef.index

    df_coef.columns = ["Intercept"] + exog.columns.tolist()

    plt.figure(figsize=(13, 7))
    sns.heatmap(
        df_coef.iloc[:, 1:],
        cmap="PiYG_r",
        square=False,
        center=0,
        annot=df_pval.iloc[:, 1:],
    )
    plt.title("Full univariate results")
    plt.annotate(
        f"""
    * Value in each cell is Bonferroni corrected p-value.
    ** {sig_key[0][0]} is significant at multivatiate level.
       p = {sig_key[0][1]}""",
        (0, 0),
        (0, -70),
        xycoords="axes fraction",
        textcoords="offset points",
        va="top",
    )
    plt.tight_layout()
    plt.savefig(f"{basepath}/univeriate.png", dpi=300, transparent=True)
    return df_coef


if __name__ == "__main__":
    mriq_drop = ["mriq_19", "mriq_22"]
    data = Data(
        datapath=DATA,
        mriq_labeltype="stats",
        mriq_drop=None,
    )
    diff = cap_pairs(data).apply(zscore)
    dur = data.load("dur").apply(zscore)
    occ = data.load("occ").apply(zscore)
    mriq = data.load("mriq_").apply(zscore)  # independent
    dataset = pd.concat([mriq, diff, dur, occ], axis=1)

    with open("results/mmr/cap_dur/univeriate_report.txt", "w") as f:
        sys.stdout = f
        _ = mmr_with_fig(mriq, dur, dataset, "results/mmr/cap_dur")
    with open("results/mmr/cap_dur/univeriate_report.txt", "w") as f:
        sys.stdout = f
        _ = mmr_with_fig(mriq, occ, dataset, "results/mmr/cap_occ")
    with open("results/mmr/cap_dur/univeriate_report.txt", "w") as f:
        sys.stdout = f
        _ = mmr_with_fig(mriq, diff, dataset, "results/mmr/cap_diff")
