# Great Britain Crime & Commuters Analysis

This repository provides data and scripts to explore the relationship between population, commuter inflows, and crime in Great Britain. There are two main Python scripts:

1. **`commuters_map_plot.py`**  
   Generates a map visualization showing commuter flows or distributions across Great Britain.

2. **`crime_regression.py`**  
   Performs regression analyses (Scaling, Cobb-Douglas, and Translog) on crime totals versus population and commuters.

---

## Data

- **Crime Data**  
  City-level or local-authority-level crime totals.
- **Commuter Data**  
  Daily commuter inflows by city.
- **Population Data**  
  Local authority population figures in Great Britain.
- **Population Matrix Data**  
  Local authority population figuring cities from Great Britain showing commuters.



These datasets should be placed in the `data/` folder:
- `data/crime_totals_scot.csv`
- `data/incoming_commuters.csv`
- `data/population_matrix.csv`
- `data/population_sorted.csv`

---

## How to Run

1. **Install Python Dependencies**

Make sure you have **Python 3.x** and the required packages installed:

```bash
pip install -r requirements.txt
```

2. **Run the Scripts**

   - **Great Britain Commuters Map**
   ```bash
   python commuters_map_plot.py
   ```

    - **Crime Regression**
   ```bash
   python crime_regression.py
   ```
