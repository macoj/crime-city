# Great Britain Crime & Commuters Analysis

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

Make sure you have **Python 3.x** and the required packages installed:

   ```bash
python pipeline.py
   ```

This script will:
-	Filter and aggregate offence data by quarter.
-	Preprocess and match LAD data to CSP data.
-	Merge duplicated CSPs in the population matrix.
-	Plot the commuting map. 
- Plot the crime regression results.

---

## TODO

- As _population_sorted.csv_ contains LAD values, it must be preprocessed in the same way as the Crime Data and Population Matrix.