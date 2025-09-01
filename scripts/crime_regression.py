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


def ridge_regression_metrics(model, x_values, y_true):
    """
    Calculate and display the R-squared, Mean Squared Error (MSE), and Bayesian Information Criterion (BIC)
    for a given ridge regression model.

    :param model: Fitted Ridge regression model.
    :param x_values: Independent variables (features) used for the model.
    :param y_true: True dependent variable values (target).
    :return: Dictionary containing R-squared, MSE, and BIC.
    """
    # Predict values
    y_pred = model.predict(x_values)

    # Calculate metrics
    r_squared = model.score(x_values, y_true)
    mse = np.mean((y_true - y_pred) ** 2)
    n_params = len(model.coef_) + 1  # Number of coefficients + intercept
    n_samples = len(y_true)
    bic = n_samples * np.log(mse) + n_params * np.log(n_samples)

    # Print metrics
    print(f"R-squared: {r_squared:.4f}")
    print(f"MSE: {mse:.4f}")
    print(f"BIC: {bic:.4f}")

    # Return metrics as a dictionary
    return {
        "R-squared": r_squared,
        "MSE": mse,
        "BIC": bic
    }


def ols(data_theft):
    Y = np.log10(data_theft[[1]]).values  # Ensure Y is a 2D array
    X = np.log10(data_theft[[0]]).values  # Ensure X is a 2D array

    alpha = 1.0
    ridge_scaling = Ridge(alpha=alpha).fit(X=X, y=Y)


def plot(df, ridge_translog):
    min_max = df[["log_CrimeTotal"]].min().values, df[["log_CrimeTotal"]].max().values
    plt.figure(figsize=(3, 2.9))
    plt.plot(df[["log_CrimeTotal"]],
             ridge_translog.predict(df[["log_Population", "log_Commuters", "log_Interaction"]]),
             lw=0, marker="."
             )
    plt.plot([min_max[0], min_max[1]], [min_max[0], min_max[1]], )
    plt.xlim(min_max)
    plt.ylim(min_max)
    plt.locator_params(axis='x', nbins=6)


def run_scaling_model(final_df, alpha=1.0):
    """Fit the Scaling model: log(Crime) ~ α + β*log(Population)."""
    X_scaling = final_df[["log_Population"]]
    y = final_df["log_CrimeTotal"]
    ridge_scaling = Ridge(alpha=alpha).fit(X_scaling, y)
    aic_scaling, bic_scaling = calculate_aic_bic(y, ridge_scaling.predict(X_scaling), 2)
    return ridge_scaling, aic_scaling, bic_scaling


def run_cobb_douglas_model(final_df, alpha=1.0):
    """Fit the Cobb-Douglas model: log(Crime) ~ α + β_P*log(Population) + β_C*log(Commuters)."""
    X_cobb = final_df[["log_Population", "log_Commuters"]]
    y = final_df["log_CrimeTotal"]
    ridge_cobb = Ridge(alpha=alpha).fit(X_cobb, y)
    aic_cobb, bic_cobb = calculate_aic_bic(y, ridge_cobb.predict(X_cobb), 3)
    return ridge_cobb, aic_cobb, bic_cobb




def run_translog_model(final_df, alpha=1.0):
    """
    Fit the Translog model: log(Crime) ~ α + β_P*log(Population) + β_C*log(Commuters)
                                  + interaction + squared terms.
    """
    # Create second-order terms
    # final_df["log_Commuters_Sq"] = final_df["log_Commuters"] ** 2
    # final_df["log_Population_Sq"] = final_df["log_Population"] ** 2
    final_df["log_Interaction"] = final_df["log_Commuters"] * final_df["log_Population"]

    X_translog = final_df[[
        "log_Population", "log_Commuters", "log_Interaction",
        # "log_Commuters_Sq", "log_Population_Sq"
    ]]
    y = final_df["log_CrimeTotal"]
    ridge_translog = Ridge(alpha=alpha).fit(X_translog, y)
    aic_translog, bic_translog = calculate_aic_bic(y, ridge_translog.predict(X_translog), 4)
    return ridge_translog, aic_translog, bic_translog



def plot_and_report_results(
        output_path,
        final_df, crime,
        ridge_scaling, aic_scaling, bic_scaling,
        ridge_cobb, aic_cobb, bic_cobb,
        ridge_translog, aic_translog, bic_translog
):
    fig, axes = plt.subplots(ncols=4, figsize=(20, 5))

    # 1) Scaling Model Plot
    beta_population = ridge_scaling.coef_[0]

    sns.regplot(
        x=final_df["log_Population"], y=final_df["log_CrimeTotal"],
        ax=axes[0], scatter_kws={"alpha": 0.6}
    )
    axes[0].set_xlabel("Log(Population)")
    axes[0].set_ylabel("Log(Crime Total)")
    axes[0].set_title("Scaling Model")
    # axes[0].set_ylim(4, 12)
    axes[0].text(
        0.05, 0.8, f"β_P = {beta_population:.2f}",
        transform=axes[0].transAxes, fontsize=14,
        bbox=dict(facecolor='white', alpha=0.5)
    )

    # 2) Cobb-Douglas Model Plot
    beta_population = ridge_cobb.coef_[0]
    beta_commuters = ridge_cobb.coef_[1]

    final_df["Cobb_Douglas_Input"] = (
            beta_population * final_df["log_Population"] +
            beta_commuters * final_df["log_Commuters"]
    )
    sns.regplot(
        x=final_df["Cobb_Douglas_Input"], y=final_df["log_CrimeTotal"],
        ax=axes[1], scatter_kws={"alpha": 0.6}
    )
    axes[1].set_xlabel("β_C * log(Commuters) + β_P * log(Population)")
    axes[1].set_ylabel("")
#     axes[1].set_ylim(4, 12)
    axes[1].set_title("Cobb-Douglas Model")
    axes[1].text(
        0.05, 0.8, f"β_C = {beta_commuters:.2f}\nβ_P = {beta_population:.2f}",
        transform=axes[1].transAxes, fontsize=14,
        bbox=dict(facecolor='white', alpha=0.5)
    )

    # 3) Translog Model Plot
    beta_population = ridge_translog.coef_[0]
    beta_commuters = ridge_translog.coef_[1]
    beta_interaction = ridge_translog.coef_[2]

    final_df["Translog_Input"] = ridge_translog.predict(
        final_df[[
            "log_Population", "log_Commuters", "log_Interaction",
            # "log_Commuters_Sq", "log_Population_Sq" ## ?
        ]]
    )
    sns.regplot(
        x=final_df["Translog_Input"], y=final_df["log_CrimeTotal"],
        ax=axes[2], scatter_kws={"alpha": 0.6}
    )
    axes[2].set_xlabel("β_P * log(Population) + β_C * log(Commuters)")
    axes[2].set_ylabel("")
#     axes[2].set_ylim(4, 12)
    axes[2].set_title("Translog Model")
    beta_coeffs = ridge_translog.coef_
    axes[2].text(
        0.05, 0.8,
        f"β_C = {beta_commuters:.2f}\nβ_P = {beta_population:.2f}\nβ_Interaction = {beta_interaction:.2f}",
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
    # axes[3].set_xticklabels(axes[3].get_xticklabels(), rotation=360)

    plt.tight_layout()
    plt.savefig(f'{output_path}/scaling_vs_cobb_translog_deltas_{crime}.pdf')
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
def plot_population_commuters_crime(final_df, output_path, size_mapping=None):
    """Generate a scatter plot for Population vs Commuters with Crime levels as point sizes."""
    if size_mapping is None:
        size_mapping = {
            20: 20,
            40: 40,
            60: 60,
            80: 80,
            100: 100
        }

    # Define number of cuts from the size_mapping
    num_cuts = len(size_mapping)

    # Define crime level brackets
    crime_levels = pd.qcut(final_df["log_CrimeTotal"], q=num_cuts, labels=list(size_mapping.keys()))

    # Map size for the markers
    final_df["Marker_Size"] = crime_levels.map(size_mapping)

    # Scatter plot
    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(
        x=final_df["log_Population"],
        y=final_df["log_Commuters"],
        s=final_df["Marker_Size"],
        alpha=0.5,
        c=final_df["log_CrimeTotal"],
        cmap='coolwarm',
        edgecolor='k'
    )

    plt.title("Log-Log plot: Population vs Commuters with Crime Levels", fontsize=16)
    plt.xlabel("Log(Population)", fontsize=14)
    plt.ylabel("Log(Commuters)", fontsize=14)

    # Add colorbar for crime levels
    colorbar = plt.colorbar(scatter)
    colorbar.set_label("Log(Crime Total)", fontsize=12)

    plt.grid(True, linestyle="--", alpha=0.6)
    plt.tight_layout()
    plt.savefig(f"{output_path}/population_commuters_crime_scatter.pdf", dpi=300)
    plt.show()


def crime_regression_plot(output_path):
    commuting_df = pd.read_csv(PREPROCESSED_POPULATION_MATRIX_CSV)
    crime_df = pd.read_csv(PREPROCESSED_CRIME_DATA_CSV)
    population_df = pd.read_csv(PREPROCESSED_CSP_POPULATION_CSV)

    # removing the diagonal (i.e., intra-city commuting)
    commuting_df = commuting_df.set_index("City")
    np.fill_diagonal(commuting_df.values, 0)

    # removing City of London
    commuting_df.drop("City of London", axis=0, inplace=True, errors='ignore')
    commuting_df.drop("City of London", axis=1, inplace=True, errors='ignore')

    commuting_df.reset_index(inplace=True)

    commuting_df.rename(columns={"Unnamed: 0": "City"}, inplace=True)
    incoming_commuters = commuting_df.set_index("City").sum(axis=0).reset_index()
    incoming_commuters.columns = ["City", "Total_Commuters"]
    merged_df = crime_df.merge(incoming_commuters, left_on="CSP Name", right_on="City", how="inner")

    final_df = merged_df.copy()
    population_df.rename(columns={"Local Authority": "CSP Name"}, inplace=True)
    final_df = final_df.merge(population_df[["CSP Name", "Population"]], on="CSP Name", how="inner")

    # Apply log10 transformation
    final_df["log_CrimeTotal"] = np.log10(final_df['Number of Offences'] + 1)
    final_df["log_Commuters"] = np.log10(final_df["Total_Commuters"])
    final_df["log_Population"] = np.log10(final_df["Population"])
    final_df.dropna(inplace=True)

    final_df.to_csv(f"{output_path}/final_df.csv")

    # === Fit each model via newly defined functions ===
    ridge_scaling, aic_scaling, bic_scaling = run_scaling_model(final_df)
    ridge_cobb, aic_cobb, bic_cobb = run_cobb_douglas_model(final_df)
    ridge_translog, aic_translog, bic_translog = run_translog_model(final_df)

    # === Generate scatter plot ===
    # plot_population_commuters_crime(final_df, output_path)

    # === Plot everything together & print statistics ===
    plot_and_report_results(
        output_path,
        final_df, 'offences',
        ridge_scaling, aic_scaling, bic_scaling,
        ridge_cobb, aic_cobb, bic_cobb,
        ridge_translog, aic_translog, bic_translog
    )
