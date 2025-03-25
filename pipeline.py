from scripts.crime_regression import crime_regression_plot
from scripts.preprocess_matrix_duplicated_cities import merge_population_matrix_duplicated_cities
from scripts.commuters_map_plot import plot_commuting_map
from scripts.filter_offences_and_aggregate_by_quarter import filter_offences_and_aggregate_by_quarter
from scripts.lad_to_csp_commuting_matrix import lad_to_csp_commuting_matrix_preprocess

from lib.logger import success


def run_pipeline():
    pipeline_steps = [
        (
            "Filtering offences and aggregating by quarter",
            filter_offences_and_aggregate_by_quarter
        ),
        (
            "Preprocessing and Matching LAD to CSP on commuting matrix and crime data",
            lad_to_csp_commuting_matrix_preprocess
        ),
        (
            "Merging duplicated CSPs in population matrix",
            merge_population_matrix_duplicated_cities
        ),
        (
            "Plotting Commuting Map",
            plot_commuting_map
        ),
        (
            "Plotting Crime Regression",
            crime_regression_plot
        ),
    ]

    for index, (step_name, step_function) in enumerate(pipeline_steps):
        success(f"\nExecuting step {index}: {step_name}...")
        step_function()

    success("Pipeline execution completed successfully.")


if __name__ == "__main__":
    run_pipeline()
