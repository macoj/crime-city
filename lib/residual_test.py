# residual_test.py
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr, laplace, kstest

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


def _laplace_plot(sami, out_path, tag):
    loc, scale = laplace.fit(sami)
    D, p = kstest(sami, 'laplace', args=(loc, scale))

    fig, ax = plt.subplots(figsize=(7, 5))
    sns.histplot(sami, bins=30, stat="density", color="skyblue",
                 edgecolor="k", alpha=0.7, ax=ax)
    xx = np.linspace(sami.min(), sami.max(), 400)
    ax.plot(xx, laplace.pdf(xx, loc=loc, scale=scale), 'r-', lw=2,
            label=f"Laplace fit\nμ={loc:.3f}, b={scale:.3f}\nKS D={D:.3f}, p={p:.2g}")
    ax.set_xlabel("SAMI (Residuals, population-only model)")
    ax.set_ylabel("Probability density")
    ax.set_title("Distribution of SAMIs with Laplace fit")
    ax.legend()
    fig.tight_layout()
    fig.savefig(f"{out_path}/sami_laplace_{tag}.pdf", dpi=300)
    plt.show()
    plt.close(fig)
    return {"laplace_mu": loc, "laplace_b": scale, "ks_D": D, "ks_p": p}


def _rank_plot(final_df, sami, out_path, tag, top_k=10):
    rank_df = pd.DataFrame({
        "CSP": final_df["CSP Name"].values if "CSP Name" in final_df.columns else np.arange(len(sami)),
        "SAMI": sami
    }).sort_values("SAMI", ascending=False).reset_index(drop=True)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    colors = np.where(rank_df["SAMI"] >= 0, "#b2182b", "#2166ac")  # red for above, blue for below
    ax.bar(rank_df.index, rank_df["SAMI"], color=colors, width=1.0)
    ax.set_xlim(0, len(rank_df)-1)
    ax.set_xlabel("Rank (high → low SAMI)")
    ax.set_ylabel("SAMI")
    ax.set_title("Rank-ordered SAMIs (population-only)")
    fig.tight_layout()
    fig.savefig(f"{out_path}/sami_rank_{tag}.pdf", dpi=300)
    plt.show()
    plt.close(fig)

    return {
        "top": rank_df.head(top_k)[["CSP", "SAMI"]].to_dict(orient="records"),
        "bottom": rank_df.tail(top_k)[["CSP", "SAMI"]].to_dict(orient="records"),
    }


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

    summary = {"n": len(sami_scaling)}

    summary["laplace"] = _laplace_plot(sami_scaling, output_path, crime_tag)
    summary["rank"] = _rank_plot(final_df, sami_scaling, output_path, crime_tag)

    def _one_compare(tag, yhat_with_commuters):
        sami_comm = _residuals(y, yhat_with_commuters)

        r, p = pearsonr(sami_scaling, sami_comm)
        var_ratio = np.var(sami_comm, ddof=1) / np.var(sami_scaling, ddof=1)
        fig, ax = plt.subplots(figsize=(6.5, 4))
        sns.kdeplot(sami_scaling, ax=ax, lw=2, label="Population-only")
        sns.kdeplot(sami_comm, ax=ax, lw=2, label=tag)
        ax.set_title("Residual distributions (SAMI)")
        ax.set_xlabel("Residual")
        ax.legend()
        fig.tight_layout()
        fig.savefig(f"{output_path}/sami_kde_{crime_tag}_scaling_vs_{tag}.pdf", dpi=300)
        plt.show()
        plt.close(fig)

        print(f"[SAMI] scaling vs {tag}: r={r:.3f}, p={p:.2g}, VarRatio={var_ratio:.2f}")

        return {"r": r, "p": p, "variance_ratio": var_ratio}

    if ridge_cobb is not None:
        yhat_cobb = ridge_cobb.predict(final_df[["log_Population", "log_Commuters"]])
        summary["scaling_vs_cobb"] = _one_compare("cobb", yhat_cobb)

    if ridge_translog is not None:
        X = final_df[["log_Population", "log_Commuters", "log_Interaction"]]
        yhat_trans = ridge_translog.predict(X)
        summary["scaling_vs_translog"] = _one_compare("translog", yhat_trans)

    pd.DataFrame({
        "CSP": final_df.get("CSP Name", pd.Series(np.arange(len(sami_scaling)))),
        "SAMI_scaling": sami_scaling
    }).to_csv(f"{output_path}/sami_scaling_{crime_tag}.csv", index=False)

    return summary
