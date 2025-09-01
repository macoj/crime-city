"""
Default offence codes used for filtering and analysis in crime datasets are:

OFFENCE_CODES = [
    # Burglary
    "28A", "30A",
    # Theft
    "39", "49"
]

These codes correspond to selected categories of:
- Burglary (dwelling and non-dwelling, only outcome)
- Theft

The descriptions for each code can be found in `lib.helpers.offence_dict`.
"""
OFFENCE_CODES = [
    # Burglary
    # "28A", "30A",
    # Theft
    "39", "49"
]

PREPROCESSED_LAD_INFORMATION_CSV = 'data/preprocessed/lad_information.csv'
PREPROCESSED_POPULATION_MATRIX_CSV = 'data/preprocessed/population_matrix.csv'
PREPROCESSED_CRIME_DATA_CSV = 'data/preprocessed/crime_data_by_csp.csv'
PREPROCESSED_CSP_LOCATIONS = 'data/preprocessed/csp_locations.csv'
PREPROCESSED_CSP_POPULATION_CSV = 'data/preprocessed/csp_population.csv'

SHOW_CSP_NAMES_ON_PLOT = False

LOG_MATCHING_CSPS_DATA = True
