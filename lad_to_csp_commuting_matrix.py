import pandas as pd
from lib.logger import info, warning, success


def load_data():
    lad_information = pd.read_csv('data/lad_information.csv', delimiter=';')
    lad_to_csp = pd.read_csv('data/lad_to_csp.csv', delimiter=';')

    lad_information['lad-code'] = lad_information['lad-code'].astype(str).str.strip()
    lad_to_csp['lad-code'] = lad_to_csp['lad-code'].astype(str).str.strip()

    success("'Lad Information' and 'Lad to CSP' data loaded")
    return lad_information, lad_to_csp


def merge_data(local_auth, lad_to_csp):
    local_auth_csps = local_auth.merge(lad_to_csp, on='lad-code', how='left')
    success("'Lad Information' and 'Lad to CSP'data merged (on: lad-code, how: left)")
    return local_auth_csps


def fix_csp_names(local_auth_csps):
    fix_csp_names_dict = {
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
        'North Devon': 'Northern Devon',
        'Northern Devon': 'Northern Devon',
    }
    local_auth_csps['csp-name'] = local_auth_csps.apply(
        lambda row: fix_csp_names_dict[row['nice-name']].strip('"') if row['nice-name'] in fix_csp_names_dict else row['csp-name'],
        axis=1
    )

    return local_auth_csps


def preprocessing_population_matrix(local_auth_csps):
    fix_lad_names_dict = {
        'Hackney, London': 'Hackney',
        'Haringey, London': 'Haringey',
        'Havering, London': 'Havering',
        'Tower Hamlets, London': 'Tower Hamlets',
        'Westminster City of London': 'Westminster',
        'Rhondda Cynon Taf': 'Rhondda Cynon Taff',
        'Bristol': 'City of Bristol',
        'Scottish Borders': 'The Scottish Borders',
        'Wyre, Lancashire': 'Wyre',
        'Lincoln': 'City of Lincoln',
        "King's Lynn and West Norfolk": 'Kings Lynn and West Norfolk',
        'Shepway': 'Folkestone and Hythe',  # Alt Name
        'Elmbridge, Surrey': 'Elmbridge',
        'Waverley, Surrey': 'Waverley',
    }

    # Read the existing population matrix
    pop_matrix = pd.read_csv("data/population_matrix.csv")

    # Track assigned CSPs and ignored LAs
    csps = []
    ignored_lads = []

    # Replace the City (LA) with its CSP
    for i, lad in enumerate(pop_matrix["City"]):
        # Apply known name fixes if any
        fixed_lad = fix_lad_names_dict.get(lad, lad)

        # Attempt to match either the raw or fixed LA name
        match = local_auth_csps[local_auth_csps["nice-name"].isin([lad, fixed_lad])]
        if not match.empty:
            csp_name = match["csp-name"].values[0]
            if pd.notna(csp_name):
                # Overwrite the LA name in 'City' with the CSP name
                pop_matrix.at[i, "City"] = csp_name
                csps.append(csp_name)
        else:
            ignored_lads.append(lad)

    pop_matrix.to_csv("data/population_matrix_by_csv.csv", index=False)

    info("\nUpdated matrix saved to 'data/population_matrix_by_csv.csv'.")

    return csps, ignored_lads


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
    updated_df = pd.read_csv("data/population_matrix_by_csv.csv")
    matrix_csps = updated_df["City"].unique().tolist()

    # 2) Read the crime totals CSV and get unique CSPs
    crime_totals = pd.read_csv("data/crime_data_by_csp.csv")
    crime_totals_csps = crime_totals["CSP Name"].unique().tolist()

    # --- Compare the two sets (Matrix CSPs vs. Crime Data CSPs) ---

    # a) How many matrix CSPs appear in crime_data_by_csp?
    matrix_in_crime = [c for c in matrix_csps if c in crime_totals_csps]
    success(f"\nMatrix CSPs count: {len(matrix_csps)}")
    success(f"Crime Data CSPs count: {len(crime_totals_csps)}")
    success(f"Matrix CSPs also in Crime Data: {len(matrix_in_crime)}")

    # b) Which Matrix CSPs are NOT in crime_data_by_csp?
    not_found_in_crime_data = [c for c in matrix_csps if c not in crime_totals_csps]
    for csp in not_found_in_crime_data:
        # If it's likely outside England/Wales, highlight in red
        if csp in non_england_wales_csp:
            warning(f"\033[91mMatrix CSP not found in Crime Data: {csp} (Not from England or Wales)\033[0m")
        else:
            info(f"Matrix CSP not found in Crime Data: {csp}")

    # c) Which Crime Data CSPs are NOT in the Matrix?
    not_found_in_matrix = [c for c in crime_totals_csps if c not in matrix_csps]
    for csp in not_found_in_matrix:
        info(f"Crime Data CSP not found in Matrix: {csp}")


def main():
    local_auth, lad_to_csp = load_data()

    local_auth_csps = merge_data(local_auth, lad_to_csp)

    local_auth_csps = fix_csp_names(local_auth_csps)

    csps, ignored_lads = preprocessing_population_matrix(local_auth_csps)

    check_matching_csps()


if __name__ == '__main__':
    main()
