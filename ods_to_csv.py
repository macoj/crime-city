import pandas as pd

# Define the offence codes you’re interested in
OFFENCE_CODES = [
    # Robbery
    "34A",  # Robbery of business property
    "34B",  # Robbery of personal property
    # Burglary
    "29",   # Aggravated burglary in a dwelling
    "28A",  # Burglary in a dwelling
    "28B",  # Attempted burglary in a dwelling
    "28C",  # Distraction burglary in a dwelling
    "28D",  # Attempted distraction burglary in a dwelling
    "31",   # Aggravated burglary in a building other than a dwelling
    "30A",  # Burglary in a building other than a dwelling
    "30B",  # Attempted burglary in a building other than a dwelling
    # Theft
    "39",   # Theft from the person
]


def read_excel_in_batches(file_path, sheet_index, chunk_size, output_csv):
    """
    Reads an Excel file in batches from the specified sheet (by index).
    Keeps consistent column names, filters by OFFENCE_CODES, and appends to one CSV.
    """

    start_row = 0
    batch_number = 0
    file_created = False  # Whether we've created/added to the CSV yet
    col_names = None      # Will store column headers from the first batch

    while True:
        # For the first batch, parse headers (header=0).
        # For subsequent batches, read as raw data (header=None) + specify 'names=col_names'.
        if batch_number == 0:
            df_chunk = pd.read_excel(
                file_path,
                sheet_name=sheet_index,
                engine="openpyxl",
                skiprows=start_row,
                nrows=chunk_size,
                header=0  # read the column headers from the first row
            )
            # Store the column names from the first batch
            col_names = df_chunk.columns
        else:
            df_chunk = pd.read_excel(
                file_path,
                sheet_name=sheet_index,
                engine="openpyxl",
                skiprows=start_row,
                nrows=chunk_size,
                header=None,     # do not treat any row as headers now
                names=col_names  # reuse column headers from the first batch
            )

        # If no data is returned, we've reached the end of the sheet
        if df_chunk.empty:
            break

        # Filter rows by the "Offence Code" column
        # Make sure the column name matches exactly what's in col_names
        # df_filtered = df_chunk[df_chunk["Offence Code"].isin(OFFENCE_CODES)]

        # Determine write mode: 'w' if we haven't written yet, otherwise 'a'
        write_mode = 'w' if not file_created else 'a'
        # Write headers only on the first write
        df_chunk.to_csv(output_csv, mode=write_mode, index=False, header=(not file_created))

        file_created = True

        # Log progress
        print(f"Batch {batch_number} | Rows read: {len(df_chunk)} | Filtered: {len(df_chunk)}")

        # Prepare for the next batch
        batch_number += 1
        start_row += chunk_size

    if file_created:
        print(f"\nAll matching rows saved to: {output_csv}")
    else:
        print("\nNo matching rows found; CSV was not created.")


if __name__ == "__main__":
    file_path = "../crime-city-data/prc-csp-1112-1415-tables.xlsx"
    sheet_index = 1  # zero-based index => 1 = second sheet
    chunk_size = 1000  # rows to read per batch
    output_csv = "filtered_offences.csv"

    read_excel_in_batches(file_path, sheet_index, chunk_size, output_csv)
