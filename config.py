"""
Default offence codes used for filtering and analysis in crime datasets are:

OFFENCE_CODES = [
    # Robbery
    "34A", "34B",
    # Burglary
    "29", "28A", "28B", "28C", "28D", "31", "30A", "30B",
    # Theft
    "39",
]

These codes correspond to selected categories of:
- Robbery (business and personal property)
- Burglary (dwelling and non-dwelling, including attempts and distraction)
- Theft (from the person)

The descriptions for each code can be found in `lib.helpers.offence_dict`.
"""
OFFENCE_CODES = [
    # Robbery
    "34A", "34B",
    # Burglary
    "29", "28A", "28B", "28C", "28D", "31", "30A", "30B",
    # Theft
    "39",
]

PREPROCESSED_LAD_INFORMATION_CSV = 'data/preprocessed/lad_information.csv'
PREPROCESSED_POPULATION_MATRIX_CSV = 'data/preprocessed/population_matrix.csv'
PREPROCESSED_CRIME_DATA_CSV = 'data/preprocessed/crime_data_by_csp.csv'
PREPROCESSED_CSP_LOCATIONS = 'data/preprocessed/csp_locations.csv'
PREPROCESSED_CSP_POPULATION_CSV = 'data/preprocessed/csp_population.csv'

SHOW_CSP_NAMES_ON_PLOT = True

LOG_MATCHING_CSPS_DATA = True
