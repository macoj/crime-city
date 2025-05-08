# England and Wales Commuters Crime Analysis

This repository provides data and scripts to explore the relationship between population, commuter inflows, and crime in England and Wales.

## Data

#### WIP

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
- [ ] Check if we need to include the probability distributions plot (elasticity)
- [ ] Improve Plots quality
