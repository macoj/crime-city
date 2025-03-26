import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge

from config import PREPROCESSED_POPULATION_MATRIX_CSV, PREPROCESSED_CRIME_DATA_CSV, PREPROCESSED_CSP_POPULATION_CSV
from lib.helpers import seaborn_styles

seaborn_styles(sns)


def calculate_aic_bic(y_true, y_pred, n_params):
    n = len(y_true)
    residual = y_true - y_pred
    mse = np.mean(residual ** 2)
    aic = n * np.log(mse) + 2 * n_params
    bic = n * np.log(mse) + n_params * np.log(n)
    return aic, bic


def run_scaling_model(final_df):
    """Fit the Scaling model: log(Crime) ~ α + β*log(Population)."""
    X_scaling = final_df[["log_Population"]]
    y = final_df["log_CrimeTotal"]
    ridge_scaling = Ridge(alpha=1.0).fit(X_scaling, y)
    aic_scaling, bic_scaling = calculate_aic_bic(y, ridge_scaling.predict(X_scaling), 2)
    return ridge_scaling, aic_scaling, bic_scaling


def run_cobb_douglas_model(final_df):
    """Fit the Cobb-Douglas model: log(Crime) ~ α + β_C*log(Commuters) + β_P*log(Population)."""
    X_cobb = final_df[["log_Commuters", "log_Population"]]
    y = final_df["log_CrimeTotal"]
    ridge_cobb = Ridge(alpha=1.0).fit(X_cobb, y)
    aic_cobb, bic_cobb = calculate_aic_bic(y, ridge_cobb.predict(X_cobb), 3)
    return ridge_cobb, aic_cobb, bic_cobb


def run_translog_model(final_df):
    """
    Fit the Translog model: log(Crime) ~ α + β_C*log(Commuters) + β_P*log(Population)
                                  + interaction + squared terms.
    """
    # Create second-order terms
    final_df["log_Commuters_Sq"] = final_df["log_Commuters"] ** 2
    final_df["log_Population_Sq"] = final_df["log_Population"] ** 2
    final_df["log_Interaction"] = final_df["log_Commuters"] * final_df["log_Population"]

    X_translog = final_df[[
        "log_Commuters", "log_Population", "log_Interaction",
        "log_Commuters_Sq", "log_Population_Sq"
    ]]
    y = final_df["log_CrimeTotal"]
    ridge_translog = Ridge(alpha=1.0).fit(X_translog, y)
    aic_translog, bic_translog = calculate_aic_bic(y, ridge_translog.predict(X_translog), 6)
    return ridge_translog, aic_translog, bic_translog


def plot_and_report_results(
        final_df, crime,
        ridge_scaling, aic_scaling, bic_scaling,
        ridge_cobb, aic_cobb, bic_cobb,
        ridge_translog, aic_translog, bic_translog
):
    fig, axes = plt.subplots(ncols=4, figsize=(20, 5))

    # 1) Scaling Model Plot
    sns.regplot(
        x=final_df["log_Population"], y=final_df["log_CrimeTotal"],
        ax=axes[0], scatter_kws={"alpha": 0.6}
    )
    axes[0].set_xlabel("Log(Population)")
    axes[0].set_ylabel("Log(Crime Total)")
    axes[0].set_title("Scaling Model")
    axes[0].set_ylim(0, 7)
    beta_population = ridge_scaling.coef_[0]
    axes[0].text(
        0.05, 0.8, f"β_P = {beta_population:.2f}",
        transform=axes[0].transAxes, fontsize=14,
        bbox=dict(facecolor='white', alpha=0.5)
    )

    # 2) Cobb-Douglas Model Plot
    final_df["Cobb_Douglas_Input"] = (
            ridge_cobb.coef_[0] * final_df["log_Commuters"] +
            ridge_cobb.coef_[1] * final_df["log_Population"]
    )
    sns.regplot(
        x=final_df["Cobb_Douglas_Input"], y=final_df["log_CrimeTotal"],
        ax=axes[1], scatter_kws={"alpha": 0.6}
    )
    axes[1].set_xlabel("β_C * log(Commuters) + β_P * log(Population)")
    axes[1].set_ylabel("")
    axes[1].set_ylim(0, 7)
    axes[1].set_title("Cobb-Douglas Model")
    beta_commuters = ridge_cobb.coef_[0]
    beta_population = ridge_cobb.coef_[1]
    axes[1].text(
        0.05, 0.8, f"β_C = {beta_commuters:.2f}\nβ_P = {beta_population:.2f}",
        transform=axes[1].transAxes, fontsize=14,
        bbox=dict(facecolor='white', alpha=0.5)
    )

    # 3) Translog Model Plot
    final_df["Translog_Input"] = ridge_translog.predict(
        final_df[[
            "log_Commuters", "log_Population", "log_Interaction",
            "log_Commuters_Sq", "log_Population_Sq"
        ]]
    )
    sns.regplot(
        x=final_df["Translog_Input"], y=final_df["log_CrimeTotal"],
        ax=axes[2], scatter_kws={"alpha": 0.6}
    )
    axes[2].set_xlabel("β_C * log(Commuters) + β_P * log(Population)")
    axes[2].set_ylabel("")
    axes[2].set_ylim(0, 7)
    axes[2].set_title("Translog Model")
    beta_coeffs = ridge_translog.coef_
    axes[2].text(
        0.05, 0.8,
        f"β_C = {beta_coeffs[0]:.2f}\nβ_P = {beta_coeffs[1]:.2f}\nβ_Interaction = {beta_coeffs[2]:.2f}",
        transform=axes[2].transAxes, fontsize=14,
        bbox=dict(facecolor='white', alpha=0.5)
    )

    # 4) AIC/BIC Deltas Plot
    delta_metrics = pd.DataFrame({
        "ΔAIC": [aic_scaling - aic_cobb, aic_cobb - aic_translog],
        "ΔBIC": [bic_scaling - bic_cobb, bic_cobb - bic_translog]
    }, index=["Scaling - Cobb-Douglas", "Cobb-Douglas - Translog"])
    delta_metrics_long = delta_metrics.reset_index().melt(
        id_vars="index", var_name="Metric", value_name="Value"
    )
    sns.barplot(
        data=delta_metrics_long, x="index", y="Value", hue="Metric",
        ax=axes[3], palette=["#0072B2", "#E69F00"]
    )
    axes[3].set_xlabel("")
    axes[3].legend(title="Metric")
    axes[3].set_title("ΔAIC & ΔBIC Comparison")
    axes[3].set_ylabel("Δ Score")
    axes[3].axhline(y=0, color="black", linestyle="-", linewidth=0.5)
    axes[3].set_xticklabels(axes[3].get_xticklabels(), rotation=360)

    plt.tight_layout()
    plt.savefig(f'output/scaling_vs_cobb_translog_deltas_{crime}.pdf')
    plt.show()

    # === Print model equations and metric deltas ===
    print(f"\nΔAIC (Scaling - Cobb): {aic_scaling - aic_cobb:.2f}")
    print(f"ΔAIC (Cobb - Translog): {aic_cobb - aic_translog:.2f}")
    print(f"\nΔBIC (Scaling - Cobb): {bic_scaling - bic_cobb:.2f}")
    print(f"ΔBIC (Cobb - Translog): {bic_cobb - bic_translog:.2f}")

    print(f"\nScaling Model: {crime} = Population^β")
    print(f"Cobb-Douglas Model: {crime} = Commuters^β_C * Population^β_P")
    print(f"Translog Model: {crime} = Commuters^β_C * Population^β_P + Interaction + Squared Terms")

    print(f"\nMetric Differences (Cobb-Douglas - Scaling - Translog):")
    print(f"AIC Scaling: {aic_scaling:.2f}")
    print(f"AIC Cobb: {aic_cobb:.2f}")
    print(f"AIC Translog: {aic_translog:.2f}\n")

    print(f"BIC Scaling: {bic_scaling:.2f}")
    print(f"BIC Cobb: {bic_cobb:.2f}")
    print(f"BIC Translog: {bic_translog:.2f}\n")

    print(f"ΔAIC (Scaling - Cobb): {aic_scaling - aic_cobb:.2f}")
    print(f"ΔAIC (Cobb - Translog): {aic_cobb - aic_translog:.2f}\n")

    print(f"ΔBIC (Scaling - Cobb): {bic_scaling - bic_cobb:.2f}")
    print(f"ΔBIC (Cobb - Translog): {bic_cobb - bic_translog:.2f}")


# === Main script ===
def crime_regression_plot():
    commuting_df = pd.read_csv(PREPROCESSED_POPULATION_MATRIX_CSV)
    crime_df = pd.read_csv(PREPROCESSED_CRIME_DATA_CSV)
    population_df = pd.read_csv(PREPROCESSED_CSP_POPULATION_CSV)

    commuting_df.rename(columns={"Unnamed: 0": "City"}, inplace=True)
    incoming_commuters = commuting_df.set_index("City").sum(axis=0).reset_index()
    incoming_commuters.columns = ["City", "Total_Commuters"]
    merged_df = crime_df.merge(incoming_commuters, left_on="CSP Name", right_on="City", how="inner")

    final_df = merged_df.copy()
    population_df.rename(columns={"Local Authority": "CSP Name"}, inplace=True)
    final_df = final_df.merge(population_df[["CSP Name", "Population"]], on="CSP Name", how="inner")
    # Apply log transformation
    final_df["log_CrimeTotal"] = np.log1p(final_df['Number of Offences'].clip(lower=0))
    final_df["log_Commuters"] = np.log(final_df["Total_Commuters"])
    final_df["log_Population"] = np.log(final_df["Population"])
    final_df.dropna(inplace=True)

    # === Fit each model via newly defined functions ===
    ridge_scaling, aic_scaling, bic_scaling = run_scaling_model(final_df)
    ridge_cobb, aic_cobb, bic_cobb = run_cobb_douglas_model(final_df)
    ridge_translog, aic_translog, bic_translog = run_translog_model(final_df)

    # === Plot everything together & print statistics ===
    plot_and_report_results(
        final_df, 'offences',
        ridge_scaling, aic_scaling, bic_scaling,
        ridge_cobb, aic_cobb, bic_cobb,
        ridge_translog, aic_translog, bic_translog
    )
