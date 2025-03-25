import pandas as pd
from lib.logger import info, warning, success

PREPROCESSED_LAD_INFORMATION_CSV = 'data/preprocessed/lad_information.csv'
PREPROCESSED_POPULATION_MATRIX_CSV = 'data/preprocessed/population_matrix.csv'
PREPROCESSED_CRIME_DATA_CSV = 'data/preprocessed/crime_data_by_csp.csv'
PREPROCESSED_CSP_LOCATIONS = 'data/preprocessed/csp_locations.csv'


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

    crime_data = pd.read_csv("data/crime_data_by_csp.csv")

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


def check_matching_csps():
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
    success(f"\nMatrix CSPs count: {len(matrix_csps)}")
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


def main():
    load_and_merge_data()

    fix_csp_names()

    generate_csp_locations_by_lad_average()

    preprocessing_crime_data()

    preprocessing_population_matrix()

    check_matching_csps()


if __name__ == '__main__':
    main()
