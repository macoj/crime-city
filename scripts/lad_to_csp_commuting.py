import pandas as pd

from config import PREPROCESSED_LAD_INFORMATION_CSV, PREPROCESSED_CRIME_DATA_CSV, PREPROCESSED_POPULATION_MATRIX_CSV, \
    PREPROCESSED_CSP_LOCATIONS, PREPROCESSED_CSP_POPULATION_CSV, LOG_MATCHING_CSPS_DATA
from lib.helpers import NON_ENGLAND_WALES_CSP_POPULATION_CSV
from lib.logger import info, warning, success


def load_and_merge_data():
    lad_information = pd.read_csv('data/lad_information.csv', delimiter=';')
    lad_to_csp = pd.read_csv('data/lad_to_csp.csv', delimiter=';')

    lad_information['lad-code'] = lad_information['lad-code'].astype(str).str.strip()
    lad_to_csp['lad-code'] = lad_to_csp['lad-code'].astype(str).str.strip()

    success("'Lad Information' and 'Lad to CSP' data loaded")
    lad_information = lad_information.merge(lad_to_csp, on='lad-code', how='left')
    success("'Lad Information' and 'Lad to CSP'data merged (on: lad-code, how: left)")

    columns_to_drop = [
        "local-authority-code", "official-name", "start-date", "end-date", "replaced-by",
        "region", "local-authority-type", "local-authority-type-name", "county-la",
        "combined-authority", "former-gss-codes", "notes", "current-authority", "BS-6879",
        "ecode", "even-older-register-and-code", "gov-uk-slug", "area", "pop-2020", "x", "y",
        "powers", "lower-or-unitary", "mapit-area-code", "ofcom", "old-ons-la-code",
        "old-register-and-code", "open-council-data-id", "os-file", "os", "snac", "wdtk-id",
        "PFA21CD", "PFA21NM"
    ]
    lad_information = lad_information.drop(columns=columns_to_drop, errors='ignore')

    lad_information.to_csv(PREPROCESSED_LAD_INFORMATION_CSV, index=False)


def fix_csp_names():
    lad_information = pd.read_csv(PREPROCESSED_LAD_INFORMATION_CSV)

    fix_lad_to_csp_names_dict = {
        'Rhondda Cynon Taff': 'Rhondda Cynon Taf',
        'Merthyr Tydfil': 'Merthyr Tydfil',
        'Wyre Forest': 'Wyre Forest',
        'Bromsgrove': 'Bromsgrove',
        'Redditch': 'Redditch',
        'Sedgemoor': 'Sedgemoor',
        'South Somerset': 'Somerset East_South Somerset',
        'Basingstoke and Deane': 'Basingstoke and Deane',
        'Rushmoor': 'Rushmoor',
        'Hart': 'Hart',
        'Westminster': 'City of London',
        'Westminster City of London': 'City of London',
        'East Dorset': 'Dorset',
        'North Dorset': 'Dorset',
        'West Dorset': 'Dorset',
        'Weymouth and Portland': 'Dorset',  # Same District
        'Daventry': 'Daventry and South Northamptonshire',
        'South Northamptonshire': 'Daventry and South Northamptonshire',
    }
    lad_information['csp-name'] = lad_information.apply(
        lambda row: fix_lad_to_csp_names_dict[row['nice-name']].strip('"') if row['nice-name'] in fix_lad_to_csp_names_dict else row['csp-name'],
        axis=1
    )

    lad_information.to_csv(PREPROCESSED_LAD_INFORMATION_CSV, index=False)


def generate_csp_locations_by_lad_average():
    lad_information = pd.read_csv(PREPROCESSED_LAD_INFORMATION_CSV)

    # @TODO SHOULD INCLUDE A VALIDATION => IF HAS LAT AND LONG AND NO CSP NAME, INCLUDE WITH THE LAD NAME ITSELF

    csp_locations_df = lad_information
    columns_to_drop = [
        'local-authority-code', 'official-name', 'nice-name', 'lad-code', 'start-date', 'end-date',
        'replaced-by', 'nation', 'region', 'local-authority-type', 'local-authority-type-name',
        'county-la', 'combined-authority', 'alt-names', 'former-gss-codes', 'notes', 'current-authority',
        'BS-6879', 'ecode', 'even-older-register-and-code', 'gov-uk-slug', 'area', 'pop-2020', 'x', 'y',
        'powers', 'lower-or-unitary', 'mapit-area-code', 'ofcom', 'old-ons-la-code', 'old-register-and-code',
        'open-council-data-id', 'os-file', 'os', 'snac', 'wdtk-id', 'lad-name', 'csp-code', 'PFA21CD', 'PFA21NM'
    ]
    csp_locations_df = csp_locations_df.drop(columns=columns_to_drop, errors='ignore')

    csp_locations_df['lat'] = csp_locations_df['lat'].astype(str).str.replace(',', '.').astype(float)
    csp_locations_df['long'] = csp_locations_df['long'].astype(str).str.replace(',', '.').astype(float)

    df_merged = csp_locations_df.groupby('csp-name', as_index=False).agg({
        'lat': 'mean',
        'long': 'mean'
    })

    df_merged.to_csv(PREPROCESSED_CSP_LOCATIONS, index=False)


def preprocessing_crime_data():
    fix_csp_names_in_crime_data = {
        'Westminster': 'City of London', # Westminster and City of London was merged
        'Northern Devon': 'North Devon',
        'Somerset East_Mendip': 'Somerset', # @todo check it later
    }

    crime_data = pd.read_csv(PREPROCESSED_CRIME_DATA_CSV)

    crime_data["CSP Name"] = crime_data["CSP Name"].replace(fix_csp_names_in_crime_data)

    crime_data.to_csv(PREPROCESSED_CRIME_DATA_CSV, index=False)

    success(f"Preprocessed crime data saved to: {PREPROCESSED_CRIME_DATA_CSV}")


def preprocessing_population_matrix():
    lad_information = pd.read_csv(PREPROCESSED_LAD_INFORMATION_CSV)

    fix_lad_names_dict = {
        'Hackney, London': 'Hackney',
        'Haringey, London': 'Haringey',
        'Havering, London': 'Havering',
        'Tower Hamlets, London': 'Tower Hamlets',
        'Westminster City of London': 'Westminster',
        'Rhondda Cynon Taf': 'Rhondda Cynon Taff',
        'Bristol': 'City of Bristol',
        'Scottish Borders': 'The Scottish Borders', # Check it later for Commuting data
        'Wyre, Lancashire': 'Wyre',
        'Lincoln': 'City of Lincoln',
        "King's Lynn and West Norfolk": 'Kings Lynn and West Norfolk',
        'Shepway': 'Folkestone and Hythe',  # Alt Name
        'Elmbridge, Surrey': 'Elmbridge',
        'Waverley, Surrey': 'Waverley',
    }

    # Read the existing population matrix
    pop_matrix = pd.read_csv("data/population_matrix.csv")

    # Track assigned CSPs and ignored LADs for row labels (City)
    csps = []
    ignored_lads = []

    # Process the "City" column (each row)
    for i, lad in enumerate(pop_matrix["City"]):
        # Apply known name fixes if any
        fixed_lad = fix_lad_names_dict.get(lad, lad)
        # Attempt to match either the raw or fixed LAD name in lad_information
        match = lad_information[lad_information["nice-name"].isin([lad, fixed_lad])]
        if not match.empty:
            csp_name = match["csp-name"].values[0]
            if pd.notna(csp_name):
                # Overwrite the LA name in 'City' with the CSP name
                pop_matrix.at[i, "City"] = csp_name
                csps.append(csp_name)
        else:
            ignored_lads.append(lad)

    # Process the header row (column names), except for the first column "City"
    new_columns = [pop_matrix.columns[0]]  # keep "City" as is
    for col in pop_matrix.columns[1:]:
        # Apply known name fixes if any
        fixed_col = fix_lad_names_dict.get(col, col)
        match = lad_information[lad_information["nice-name"].isin([col, fixed_col])]
        if not match.empty:
            csp_name = match["csp-name"].values[0]
            new_columns.append(csp_name if pd.notna(csp_name) else col)
        else:
            new_columns.append(col)
    pop_matrix.columns = new_columns


    pop_matrix.to_csv(PREPROCESSED_POPULATION_MATRIX_CSV, index=False)
    info(f"\nUpdated matrix saved to '{PREPROCESSED_POPULATION_MATRIX_CSV}'.")


def check_matching_matrix_csps():
    info('\n---------------------------------------------------------')
    info('---------Matching CSPs (Crime vs Commuters)--------------')
    info('---------------------------------------------------------')

    non_england_wales_csp = {
        "Clackmannanshire", "Dumfries and Galloway", "East Ayrshire", "East Lothian",
        "East Renfrewshire", "Eilean Siar", "Falkirk", "Fife", "Highland", "Inverclyde",
        "Midlothian", "Moray", "North Ayrshire", "Orkney Islands", "Perth and Kinross",
        "Scottish Borders", "Shetland Islands", "South Ayrshire", "South Lanarkshire",
        "Stirling", "Aberdeen City", "Aberdeenshire", "Argyll and Bute", "City of Edinburgh",
        "Renfrewshire", "West Dunbartonshire", "West Lothian", "Angus", "Dundee City",
        "North Lanarkshire", "East Dunbartonshire", "Glasgow City",
    }

    # 1) Read the newly updated matrix where "City" is replaced by the CSP name
    updated_df = pd.read_csv(PREPROCESSED_POPULATION_MATRIX_CSV)
    matrix_csps = updated_df["City"].unique().tolist()

    # 2) Read the crime totals CSV and get unique CSPs
    crime_totals = pd.read_csv(PREPROCESSED_CRIME_DATA_CSV)
    crime_totals_csps = crime_totals["CSP Name"].unique().tolist()

    # --- Compare the two sets (Matrix CSPs vs. Crime Data CSPs) ---

    # a) How many matrix CSPs appear in crime_data_by_csp?
    matrix_in_crime = [c for c in matrix_csps if c in crime_totals_csps]
    success(f"Matrix CSPs count: {len(matrix_csps)}")
    success(f"Crime Data CSPs count: {len(crime_totals_csps)}")
    success(f"Matrix CSPs also in Crime Data CSPs: {len(matrix_in_crime)}")

    # b) Which Matrix CSPs are NOT in crime_data_by_csp?
    not_found_in_crime_data = [c for c in matrix_csps if c not in crime_totals_csps]
    for csp in not_found_in_crime_data:
        if csp in non_england_wales_csp:
            warning(f"\033[91mMatrix CSP not found in Crime Data: {csp} (Not from England or Wales)\033[0m")
        else:
            info(f"Matrix CSP not found in Crime Data CSPs: {csp}")

    # c) Which Crime Data CSPs are NOT in the Matrix?
    not_found_in_matrix = [c for c in crime_totals_csps if c not in matrix_csps]
    for csp in not_found_in_matrix:
        info(f"Crime Data CSP not found in Matrix CSPs: {csp}")


def preprocess_lad_population_to_csp():
    # Dictionary to fix known Local Authority name variations
    fix_lad_names_dict = {
        'Westminster City of London': 'City of London',
        "King’s Lynn and West Norfolk": 'Kings Lynn and West Norfolk',
        'Rotherham ': 'Rotherham',
        'Bridgend ': 'Bridgend',
        'Kirklees ': 'Kirklees',
        'Knowsley ': 'Knowsley',
        'Oldham ': 'Oldham',
        'Dudley ': 'Dudley',
        'Sandwell ': 'Sandwell',
        'York UA': 'City of York',
    }

    # 1) Load the CSVs
    lad_population = pd.read_csv("data/lad_population.csv")
    lad_information = pd.read_csv(PREPROCESSED_LAD_INFORMATION_CSV)

    # 2) Apply name fixes from the dictionary to 'Local Authority'
    lad_population["Local Authority"] = lad_population["Local Authority"].apply(
        lambda x: fix_lad_names_dict.get(x, x)
    )

    # 3) Merge on the 'Local Authority' (lad_population) and 'nice-name' (lad_information)
    merged = pd.merge(
        lad_population,
        lad_information[["nice-name", "csp-name"]],
        left_on="Local Authority",
        right_on="nice-name",
        how="left"
    )

    # 4) If a match is found (csp-name not NaN), replace 'Local Authority' with 'csp-name'
    merged["Local Authority"] = merged.apply(
        lambda row: row["csp-name"] if pd.notnull(row["csp-name"]) else row["Local Authority"],
        axis=1
    )

    # 5) Remove the suffix " UA" if it appears at the end of the Local Authority name
    merged["Local Authority"] = merged["Local Authority"].str.replace(r"\sUA$", "", regex=True)

    # 6) Drop the merge-only helper columns
    merged.drop(columns=["nice-name", "csp-name"], inplace=True)

    # 7) Merge (aggregate) any remaining duplicates in "Local Authority"
    #    For numeric columns, we sum them; for non-numeric, we keep the first value.
    #    Modify the aggregation logic as appropriate for your dataset.

    # Identify all columns except 'Local Authority'
    other_cols = [col for col in merged.columns if col != "Local Authority"]

    # Build an aggregation dictionary: sum for numeric, first for everything else
    agg_funcs = {}
    for col in other_cols:
        if pd.api.types.is_numeric_dtype(merged[col]):
            agg_funcs[col] = 'sum'
        else:
            agg_funcs[col] = 'first'

    # Group by 'Local Authority' and aggregate
    final_df = merged.groupby("Local Authority", as_index=False).agg(agg_funcs)

    # 8) Save the updated DataFrame
    final_df.to_csv(PREPROCESSED_CSP_POPULATION_CSV, index=False)

    success(f"Preprocessing complete. Updated file saved to {PREPROCESSED_CSP_POPULATION_CSV}\n")


def check_matching_population_csps():
    info('\n----------------------------------------------------------')
    info('---------Matching CSPs (Crime vs Population)--------------')
    info('----------------------------------------------------------')

    # 1) Read the newly updated lad population CSV
    updated_population = pd.read_csv(PREPROCESSED_CSP_POPULATION_CSV)
    population_csps = updated_population["Local Authority"].unique().tolist()

    # 2) Read the crime data CSV and get unique CSPs
    crime_data = pd.read_csv(PREPROCESSED_CRIME_DATA_CSV)
    crime_data_csps = crime_data["CSP Name"].unique().tolist()

    # --- Compare the two sets (Population CSPs vs. Crime Data CSPs) ---

    # a) How many population CSPs appear in crime_data?
    population_in_crime = [c for c in population_csps if c in crime_data_csps]
    success(f"Population CSV CSPs count: {len(population_csps)}")
    success(f"Crime Data CSPs count: {len(crime_data_csps)}")
    success(f"Population CSPs also in Crime Data: {len(population_in_crime)}")

    # b) Which Population CSPs are NOT in crime_data?
    not_found_in_crime_data = [c for c in population_csps if c not in crime_data_csps]
    for csp in not_found_in_crime_data:
        if csp in NON_ENGLAND_WALES_CSP_POPULATION_CSV:
            warning(f"Population CSP not found in Crime Data: {csp} (Not from England or Wales)")
        else:
            info(f"Population CSP not found in Crime Data: {csp}")

    # c) Which Crime Data CSPs are NOT in the Population CSV?
    not_found_in_population = [c for c in crime_data_csps if c not in population_csps]
    for csp in not_found_in_population:
        info(f"Crime Data CSP not found in Population CSV: {csp}")


def lad_to_csp_commuting_preprocess():
    load_and_merge_data()

    fix_csp_names()

    generate_csp_locations_by_lad_average()

    preprocessing_crime_data()

    preprocessing_population_matrix()

    if LOG_MATCHING_CSPS_DATA:
        check_matching_matrix_csps()

    preprocess_lad_population_to_csp()

    if LOG_MATCHING_CSPS_DATA:
        check_matching_population_csps()
