def seaborn_styles(sns):
    sns.set_style("whitegrid")
    sns.set(font='serif')
    sns.set_style("white", {
        "font.family": "serif",
        "font.serif": ["Times", "Palatino", "serif"],
    })


CRIME_TYPES = ['Criminal damage and arson', 'Crimes Of Dishonesty', 'Sexual offences',
               'Violence against the person', 'Other', 'Total']


NON_ENGLAND_WALES_CSP_POPULATION_CSV = {
    # --- SCOTLAND ---
    "Aberdeen City",
    "Aberdeenshire",
    "Angus",
    "Argyll and Bute",
    "Argyll & Bute",                 # alternate naming
    "Clackmannanshire",
    "Dumfries and Galloway",
    "Dumfries & Galloway",          # alternate naming
    "Dundee City",
    "East Ayrshire",
    "East Dunbartonshire",
    "East Lothian",
    "East Renfrewshire",
    "Eilean Siar",
    "Falkirk",
    "Fife",
    "Glasgow City",
    "Highland",
    "Inverclyde",
    "Midlothian",
    "Moray",
    "North Ayrshire",
    "North Lanarkshire",
    "Orkney Islands",
    "Perth and Kinross",
    "Perth & Kinross",              # alternate naming
    "Renfrewshire",
    "Scottish Borders",
    "Shetland Islands",
    "South Ayrshire",
    "South Lanarkshire",
    "Stirling",
    "West Dunbartonshire",
    "West Lothian",
    "City of Edinburgh",
    "Edinburgh, City of",           # alternate naming

    # --- NORTHERN IRELAND ---
    "Antrim",
    "Ards",
    "Armagh",
    "Ballymena",
    "Ballymoney",
    "Banbridge",
    "Belfast",
    "Carrickfergus",
    "Castlereagh",
    "Coleraine",
    "Cookstown",
    "Craigavon",
    "Down",
    "Dungannon",
    "Fermanagh",
    "Limavady",
    "Larne",
    "Lisburn",
    "Magherafelt",
    "Moyle",
    "Newry and Mourne",
    "Newtownabbey",
    "North Down",
    "Omagh",
    "Strabane",
}

offence_dict = {
    "34A": "Robbery: Robbery of business property",
    "34B": "Robbery: Robbery of personal property",
    "29": "Burglary: Aggravated burglary in a dwelling (outcome only)",
    "28B": "Burglary: Attempted burglary in a dwelling (outcome only)",
    "28D": "Burglary: Attempted distraction burglary in a dwelling (outcome only)",
    "28A": "Burglary: Burglary in a dwelling (outcome only)",
    "28C": "Burglary: Distraction burglary in a dwelling (outcome only)",
    "31": "Burglary: Aggravated burglary in a building other than a dwelling (outcome only)",
    "30B": "Burglary: Attempted burglary in a building other than a dwelling (outcome only)",
    "30A": "Burglary: Burglary in a building other than a dwelling (outcome only)",
    "39": "Theft: Theft from the person"
}
