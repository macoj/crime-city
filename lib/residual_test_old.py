# residual_test.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

sns.set_context("talk")


def _residuals(y_true, y_pred):
    return y_true - y_pred


def _scatter(ax, x, y, title, xlabel, ylabel, annotate=None):
    ax.scatter(x, y, s=25, alpha=0.6, edgecolor="none")
    lim = [min(x.min(), y.min()), max(x.max(), y.max())]
    ax.plot(lim, lim, "k-", linewidth=1)   # 45° line
    ax.set_xlim(lim); ax.set_ylim(lim)
    ax.set_title(title)
    ax.set_xlabel(xlabel); ax.set_ylabel(ylabel)
    if annotate:
        ax.text(0.02, 0.98, annotate, transform=ax.transAxes,
                va="top", ha="left",
                bbox=dict(facecolor="white", alpha=0.8, lw=0))


def residual_sami_test(
    final_df: pd.DataFrame,
    ridge_scaling,
    ridge_cobb=None,
    ridge_translog=None,
    output_path=".",
    crime_tag="offences"
):
    y = final_df["log_CrimeTotal"].values
    yhat_scaling = ridge_scaling.predict(final_df[["log_Population"]])
    sami_scaling = _residuals(y, yhat_scaling)

    outputs = {}

    def _one_compare(tag, yhat_with_commuters):
        sami_comm = _residuals(y, yhat_with_commuters)

        r, p = pearsonr(sami_scaling, sami_comm)
        var_ratio = np.var(sami_comm, ddof=1) / np.var(sami_scaling, ddof=1)

        fig, ax = plt.subplots(figsize=(5, 5))
        _scatter(
            ax,
            sami_scaling, sami_comm,
            title=f"SAMI correlation: scaling vs {tag}",
            xlabel="SAMI (population-only)",
            ylabel=f"SAMI ({tag})",
            annotate=f"r = {r:.2f}\np = {p:.2g}\nVar ratio = {var_ratio:.2f}"
        )
        fig.tight_layout()
        fig.savefig(f"{output_path}/sami_scatter_{crime_tag}_scaling_vs_{tag}.pdf", dpi=300)
        plt.close(fig)

        # ---- Plot 2: distributions
        fig, ax = plt.subplots(figsize=(6.5, 4))
        sns.kdeplot(sami_scaling, ax=ax, lw=2, label="Population-only")
        sns.kdeplot(sami_comm, ax=ax, lw=2, label=tag)
        ax.set_title("Residual distributions (SAMI)")
        ax.set_xlabel("Residual")
        ax.legend()
        fig.tight_layout()
        plt.show()
        fig.savefig(f"{output_path}/sami_kde_{crime_tag}_scaling_vs_{tag}.pdf", dpi=300)
        plt.close(fig)

        print(f"[SAMI] scaling vs {tag}: r={r:.3f}, p={p:.2g}, VarRatio={var_ratio:.2f} "
              f"(<1 means commuters reduce variance)")

        return {"r": r, "p": p, "variance_ratio": var_ratio}

    if ridge_cobb is not None:
        yhat_cobb = ridge_cobb.predict(final_df[["log_Population", "log_Commuters"]])
        outputs["scaling_vs_cobb"] = _one_compare("cobb", yhat_cobb)

    if ridge_translog is not None:
        X = final_df[["log_Population", "log_Commuters", "log_Interaction"]]
        yhat_trans = ridge_translog.predict(X)
        outputs["scaling_vs_translog"] = _one_compare("translog", yhat_trans)

    return outputs
