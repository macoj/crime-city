import pandas as pd

# 1) Read CSV, using the first row as headers
df = pd.read_csv("data/preprocessed/population_matrix.csv", header=0)

# Identify duplicated values
duplicated_cities = df["City"][df["City"].duplicated(keep=False)].unique()

for duplicated_city in duplicated_cities:
    filtered_rows = df[df["City"] == duplicated_city]

    # Print the column values for each duplicated city
    print(f"City: {duplicated_city}")
    for _, row in filtered_rows.iterrows():
        print(row.tolist()[1:])  # Remove the first value from the list before printing
    print("-" * 40)
