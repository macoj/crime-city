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

MISSING_LAD_COORDS = {
    "Aylesbury Vale": (51.8167, -0.8167),
    "Buckinghamshire County": (51.7830, -0.8000),
    "Bournemouth": (50.7192, -1.8808),
    "Christchurch": (50.7380, -1.7799),
    "Chiltern": (51.6633, -0.6333),
    "Corby": (52.4875, -0.7058),
    "Cambridgeshire and Peterborough": (52.2053, 0.1218),
    "Daventry": (52.2560, -1.1626),
    "East Dorset": (50.8421, -1.8920),
    "East Midlands CCA": (52.9548, -1.1581),
    "East Northamptonshire": (52.4380, -0.5246),
    "Forest Heath": (52.3911, 0.6469),
    "Kettering": (52.3963, -0.7304),
    "North Dorset": (50.9300, -2.3100),
    "Northampton": (52.2405, -0.9027),
    "Northamptonshire": (52.2725, -0.8930),
    "Poole": (50.7150, -1.9872),
    "Purbeck": (50.6400, -2.1000),
    "South Bucks": (51.5535, -0.5984),
    "St Edmundsbury": (52.2460, 0.7118),
    "South Northamptonshire": (52.1317, -1.0839),
    "Suffolk Coastal": (52.1453, 1.4005),
    "Taunton Deane": (51.0148, -3.1022),
    "Waveney": (52.4736, 1.7500),
    "West Dorset": (50.7469, -2.7556),
    "West of England": (51.4545, -2.5879),
    "Wellingborough": (52.3024, -0.6936),
    "Weymouth and Portland": (50.6167, -2.4500),
    "West Midlands": (52.4862, -1.8904),
    "West Somerset": (51.1530, -3.3217),
    "Wycombe": (51.6286, -0.7482),
}

OFFENCE_DICT = {
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
