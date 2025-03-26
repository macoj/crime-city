import pandas as pd
import os

from config import PREPROCESSED_CRIME_DATA_CSV, OFFENCE_CODES
from lib.logger import info, success, warning


def filter_offences_and_aggregate_by_quarter():
    # Ensure output directory exists
    os.makedirs(os.path.dirname(PREPROCESSED_CRIME_DATA_CSV), exist_ok=True)

    # Validate input parameters
    if not OFFENCE_CODES:
        warning("No offence codes provided. Exiting.")
        return

    input_file = 'data/offences.csv'
    chunk_size = 5000
    all_filtered_chunks = []
    total_read = 0
    total_filtered = 0

    try:
        # Use iterator for memory efficiency
        csv_reader = pd.read_csv(
            input_file,
            chunksize=chunk_size,
            dtype={
                'Offence Code': str,         # Ensure offence codes are read as strings
                'Financial Quarter': str,    # We'll overwrite this anyway
                'Number of Offences': float  # Make sure this is numeric so it can be summed
            }
        )

        for batch_number, df_chunk in enumerate(csv_reader, 1):
            total_read += len(df_chunk)

            # Filter rows by Offence Code
            df_filtered = df_chunk[df_chunk["Offence Code"].isin(OFFENCE_CODES)]

            if not df_filtered.empty:
                all_filtered_chunks.append(df_filtered)
                total_filtered += len(df_filtered)
                info(f"Batch {batch_number} | Read: {len(df_chunk)} | Filtered: {len(df_filtered)}")
            else:
                info(f"Batch {batch_number} | No matching rows.")

        # Combine and aggregate if any matching rows found
        if all_filtered_chunks:
            combined_df = pd.concat(all_filtered_chunks, ignore_index=True)

            # 1) Overwrite the financial quarter (optional, if you want "ALL" explicitly)
            combined_df["Financial Quarter"] = "ALL"

            # 2) Group by only CSP Name to sum across *all* quarters
            #    If you prefer to keep a "Financial Quarter" column with "ALL",
            #    you can group by ["Financial Quarter", "CSP Name"] instead.
            agg_df = (
                combined_df
                .groupby("CSP Name", dropna=False)["Number of Offences"]
                .sum()
                .reset_index(name="Number of Offences")
            )

            agg_df.to_csv(PREPROCESSED_CRIME_DATA_CSV, index=False)

            success(f"\nProcessing complete:")
            success(f"Total rows read: {total_read}")
            success(f"Total rows filtered: {total_filtered}")
            success(f"Aggregated data saved to: {PREPROCESSED_CRIME_DATA_CSV}\n")
        else:
            warning("\nNo matching rows found; CSV was not created.")

    except FileNotFoundError:
        warning(f"Input file not found: {input_file}")
    except pd.errors.EmptyDataError:
        warning(f"The input file {input_file} is empty.")
    except Exception as e:
        warning(f"An unexpected error occurred: {e}")