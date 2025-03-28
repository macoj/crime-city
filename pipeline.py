from datetime import datetime
import os

from scripts.crime_regression import crime_regression_plot
from scripts.preprocess_matrix_duplicated_cities import merge_population_matrix_duplicated_cities
from scripts.commuters_map_plot import plot_commuting_map
from scripts.filter_offences_and_aggregate_by_quarter import filter_offences_and_aggregate_by_quarter
from scripts.lad_to_csp_commuting import lad_to_csp_commuting_preprocess

from lib.logger import success
from scripts.save_config_info import save_offence_info_txt


def run_pipeline():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    experiment_dir = f"experiment_{timestamp}"
    output_path = f'output/{experiment_dir}'
    os.makedirs(output_path, exist_ok=True)

    pipeline_steps = [
        ("Filtering offences and aggregating by quarter", filter_offences_and_aggregate_by_quarter),
        ("Preprocessing and Matching LAD to CSP on commuting matrix and crime data", lad_to_csp_commuting_preprocess),
        ("Merging duplicated CSPs in population matrix", merge_population_matrix_duplicated_cities),
        ("Plotting Commuting Map", lambda: plot_commuting_map(output_path)),
        ("Plotting Crime Regression", lambda: crime_regression_plot(output_path)),
        ("Save Experiments Config", lambda: save_offence_info_txt(output_path)),
    ]

    for index, (step_name, step_function) in enumerate(pipeline_steps):
        success(f"\nExecuting step {index}: {step_name}...")
        step_function()

    success(f"Pipeline execution completed successfully. Results stored in: {output_path}")


if __name__ == "__main__":
    run_pipeline()
