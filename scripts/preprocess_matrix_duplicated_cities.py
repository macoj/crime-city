import pandas as pd
import numpy as np
from config import PREPROCESSED_POPULATION_MATRIX_CSV

def merge_population_matrix_duplicated_cities():
    matrix = pd.read_csv(PREPROCESSED_POPULATION_MATRIX_CSV, header=None).to_numpy()

    df = pd.DataFrame(matrix[1:, 1:], index=matrix[1:, 0], columns=matrix[0, 1:]).astype(int)

    duplicated_rows = df.index[df.index.duplicated()].unique()
    duplicated_cols = df.columns[df.columns.duplicated()].unique()

    for city in duplicated_rows:
        rows_to_merge = df.loc[city]
        df = df.drop(city, axis=0)
        df.loc[city] = rows_to_merge.sum()

    for city in duplicated_cols:
        cols_to_merge = df[city]
        df = df.drop(city, axis=1)
        df[city] = cols_to_merge.sum(axis=1)

    df = df.loc[df.columns, df.columns]

    # Reset the index and columns to insert the 'City' header correctly
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'City'}, inplace=True)

    # Write the DataFrame to CSV including the header
    df.to_csv(PREPROCESSED_POPULATION_MATRIX_CSV, index=False)