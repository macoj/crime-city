# England and Wales Commuters Crime Analysis

This repository provides data and scripts to explore the relationship between population, commuter inflows, and crime in England and Wales.

## Data

- [Place of Residence by Place of Work, Local Authority](https://data.london.gov.uk/dataset/place-residence-place-work-local-authority)
- [Police recorded crime Community Safety Partnership Open Data Table, from year ending March 2012 to year ending March 2015](https://www.gov.uk/government/statistics/police-recorded-crime-open-data-tables)
- [LAD to Community Safety Partnership to PFA (December 2019) Lookup in EW (2019](https://geoportal.statistics.gov.uk/datasets/8bd726c1cd5340e3980d03e0877efb3e_0)
- [UK local authorities (past and current) (2024)](https://pages.mysociety.org/uk_local_authority_names_and_codes/downloads/uk-la-past-current-uk-local-authorities-current-csv/latest#survey)
- [2011 Census: Key Statistics for Local Authorities in England and Wales](https://www.ons.gov.uk/peoplepopulationandcommunity/populationandmigration/populationestimates/datasets/2011censuskeystatisticsforlocalauthoritiesinenglandandwales)

---

## How to Run

1. **Install Python Dependencies**

Make sure you have **Python 3.x** and the required packages installed:

```bash
pip install -r requirements.txt
```

2. **Run the Pipeline**

Simply run the main pipeline script, and the output will be stored in **./output**.

   ```bash
python pipeline.py
   ```

This script will:
-	Filter and aggregate offence data by quarter.
-	Preprocess and match LAD data to CSP data.
-	Merge duplicated CSPs in the population matrix.
-	Plot the commuting map. 
-   Plot the crime regression results.

---

## TODO

- [x] As _population_sorted.csv_ contains LAD values, it must be preprocessed in the same way as the Crime Data and Population Matrix.
- [x] Analyze whether the diagonals of the commuters matrix should be considered as the total population of a city **[we removed because we already use a data for the total population of a specific CSP]**
- [x] In the preprocessed LAD_information.csv, analyze the CSPs that share the same LAD name (Buckinghamshire) but have different CSP names (Aylesbury Vale, Chiltern, South Bucks, Wycombe). This behavior is the opposite of what was intended. **[only 15 datapoints have this weird behavior, and it only affects the map plot]**