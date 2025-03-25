import duckdb


def get_unique_financial_quarters(file_path):
    """
    Query the unique values of the 'Financial Quarter' column in a CSV file using DuckDB

    Args:
        file_path (str): Path to the CSV file

    Returns:
        list: List of unique values in the 'Financial Quarter' column
    """
    try:
        # Connect to an in-memory DuckDB database
        conn = duckdb.connect(database=':memory:')

        # Query to get unique values from the 'Financial Quarter' column
        query = f"""
            SELECT DISTINCT "Financial Quarter" AS unique_quarters
            FROM read_csv_auto('{file_path}')
            ORDER BY "Financial Quarter"
        """

        # Execute the query and fetch all results
        results = conn.execute(query).fetchall()

        # Extract the values from the result tuples
        unique_quarters = [row[0] for row in results]

        return unique_quarters

    except Exception as e:
        print(f"Error: {e}")
        return None
    finally:
        # Close the connection
        if 'conn' in locals():
            conn.close()


# Example usage
if __name__ == "__main__":
    file_path = 'offences.csv'  # Replace with your actual file path
    unique_quarters = get_unique_financial_quarters(file_path)

    if unique_quarters is not None:
        print(f"Unique Financial Quarter values:")
        for quarter in unique_quarters:
            print(f"  - {quarter}")
