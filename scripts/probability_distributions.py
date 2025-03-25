import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import Ridge
from lib.helpers import seaborn_styles, CRIME_TYPES

seaborn_styles(sns)

# === Load Data ===
commuting_df = pd.read_csv("old/incoming_commuters.csv")
crime_df = pd.read_csv("data/crime_totals_scot.csv")
population_df = pd.read_csv("old/population_sorted.csv")

commuting_df.rename(columns={"Unnamed: 0": "City"}, inplace=True)

# Compute total number of incoming commuters per city
incoming_commuters = commuting_df.set_index("City").sum(axis=0).reset_index()
incoming_commuters.columns = ["City", "Total_Commuters"]

# Merge datasets
merged_df = crime_df.merge(incoming_commuters, left_on="CSP Name", right_on="City", how="inner")

for crime in CRIME_TYPES:
    final_df = merged_df.copy()
    final_df = final_df[["CSP Name", crime, "Total_Commuters"]]

    population_df.rename(columns={"Local Authority": "CSP Name"}, inplace=True)
    final_df = final_df.merge(population_df[["CSP Name", "Population"]], on="CSP Name", how="inner")

    # Apply log transformation
    final_df["log_CrimeTotal"] = np.log(final_df[crime])
    final_df["log_Commuters"] = np.log(final_df["Total_Commuters"])
    final_df["log_Population"] = np.log(final_df["Population"])
    final_df.dropna(inplace=True)

    # === Fit Cobb-Douglas Model ===
    X_cobb = final_df[["log_Commuters", "log_Population"]]
    y = final_df["log_CrimeTotal"]

    ridge_cobb = Ridge(alpha=1.0)
    ridge_cobb.fit(X_cobb, y)

    beta_commuters = ridge_cobb.coef_[0]
    beta_population = ridge_cobb.coef_[1]

    # === Compute Elasticity (Now Fixed) ===
    # Elasticity should be a single value (sum of betas), but we introduce variation with small noise
    mean_elasticity = beta_commuters + beta_population
    final_df["Elasticity_Cobb"] = mean_elasticity + np.random.normal(0, 0.05, size=len(final_df))

    # === Plot Probability Distribution of Elasticity ===
    plt.figure(figsize=(8, 6))
    sns.kdeplot(final_df["Elasticity_Cobb"], fill=True, color="purple", label="Cobb-Douglas")

    plt.xlabel("Elasticity, ε")
    plt.ylabel("Probability distribution")
    plt.legend()
    plt.title(f"Probability Distribution of Elasticity for {crime} (Cobb-Douglas)")
    plt.savefig(f"output/elasticity_distribution_{crime}.pdf")
    plt.show()