# CodeAlpha Task 2 — Unemployment Analysis with Python

## Objective
Analyze unemployment-rate data using Python, clean the dataset, explore trends, investigate the impact of COVID-19, identify regional patterns, and create visualizations.

## Files
- `unemployment_analysis.py` — complete analysis script
- `Unemployment_Rate_upto_11_2020.csv` — place the dataset here
- `requirements.txt` — Python dependencies
- `unemployment_analysis.ipynb` — notebook version
- `outputs/` — generated charts and CSV summaries

## Dataset
The project expects the commonly used CodeAlpha/Kaggle unemployment dataset with fields such as:
- Region
- Date
- Estimated Unemployment Rate (%)
- Estimated Employed
- Estimated Labour Participation Rate (%)
- Area (when available)

## How to Run

```bash
pip install -r requirements.txt
python unemployment_analysis.py
```

For Jupyter:

```bash
jupyter notebook unemployment_analysis.ipynb
```

## Analysis Included
1. Data cleaning and duplicate removal
2. Missing-value handling
3. Date conversion and time-based features
4. Overall unemployment trend
5. Before-COVID vs COVID-period comparison
6. Region-wise unemployment analysis
7. Region/date heatmap
8. Urban vs rural comparison when `Area` is present
9. Numerical summary of key findings

## GitHub Repository Name
`CodeAlpha_Unemployment_Analysis`
