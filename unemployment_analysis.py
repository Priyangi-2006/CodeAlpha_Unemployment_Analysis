"""
CodeAlpha Data Science Internship 
Unemployment Analysis with Python

Input:
    Unemployment_Rate_upto_11_2020.csv

Outputs:
    outputs/*.png
    outputs/summary_statistics.csv
    outputs/regional_summary.csv
"""

from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

DATA_FILE = Path("Unemployment_Rate_upto_11_2020.csv")
OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

if not DATA_FILE.exists():
    raise FileNotFoundError(
        f"{DATA_FILE} not found. Place the CodeAlpha unemployment CSV in this folder."
    )

df = pd.read_csv(DATA_FILE)
df.columns = df.columns.str.strip()

# Clean column names and values
df = df.drop_duplicates().copy()
for col in df.select_dtypes(include="object").columns:
    df[col] = df[col].astype(str).str.strip()

required = [
    "Region", "Date", "Estimated Unemployment Rate (%)",
    "Estimated Employed", "Estimated Labour Participation Rate (%)"
]
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

df["Date"] = pd.to_datetime(df["Date"], dayfirst=True, errors="coerce")
numeric_cols = [
    "Estimated Unemployment Rate (%)",
    "Estimated Employed",
    "Estimated Labour Participation Rate (%)"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

df = df.dropna(subset=["Date"] + numeric_cols).copy()
df["Year"] = df["Date"].dt.year
df["Month"] = df["Date"].dt.month
df["Month_Name"] = df["Date"].dt.strftime("%b")

print("\nDATASET SHAPE:", df.shape)
print("\nFIRST FIVE ROWS:")
print(df.head())
print("\nMISSING VALUES:")
print(df.isnull().sum())
print("\nSUMMARY STATISTICS:")
print(df[numeric_cols].describe())

df[numeric_cols].describe().to_csv(OUTPUT_DIR / "summary_statistics.csv")

# 1. Overall unemployment trend
monthly = (
    df.groupby("Date", as_index=False)["Estimated Unemployment Rate (%)"]
      .mean()
      .sort_values("Date")
)

plt.figure(figsize=(12, 6))
sns.lineplot(
    data=monthly,
    x="Date",
    y="Estimated Unemployment Rate (%)",
    marker="o"
)
plt.axvspan(pd.Timestamp("2020-03-01"), pd.Timestamp("2020-06-30"),
            alpha=0.15, label="COVID-19 period")
plt.title("India Unemployment Rate Trend")
plt.xlabel("Date")
plt.ylabel("Average Unemployment Rate (%)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "01_unemployment_trend.png", dpi=300)
plt.close()

# 2. COVID comparison
before_covid = df[df["Date"] < "2020-03-01"]["Estimated Unemployment Rate (%)"].mean()
covid_period = df[
    (df["Date"] >= "2020-03-01") & (df["Date"] <= "2020-06-30")
]["Estimated Unemployment Rate (%)"].mean()

covid_df = pd.DataFrame({
    "Period": ["Before COVID", "Mar-Jun 2020"],
    "Average Unemployment Rate (%)": [before_covid, covid_period]
})

plt.figure(figsize=(8, 5))
sns.barplot(data=covid_df, x="Period", y="Average Unemployment Rate (%)")
plt.title("Unemployment Rate: Before COVID vs Mar-Jun 2020")
plt.ylabel("Average Unemployment Rate (%)")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "02_covid_impact.png", dpi=300)
plt.close()

# 3. Regional analysis
regional = (
    df.groupby("Region")["Estimated Unemployment Rate (%)"]
      .agg(["mean", "max", "min"])
      .sort_values("mean", ascending=False)
)
regional.to_csv(OUTPUT_DIR / "regional_summary.csv")

plt.figure(figsize=(10, 8))
sns.barplot(
    x=regional["mean"].values,
    y=regional.index
)
plt.title("Average Unemployment Rate by Region")
plt.xlabel("Average Unemployment Rate (%)")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "03_regional_analysis.png", dpi=300)
plt.close()

# 4. Region x month heatmap
pivot = df.pivot_table(
    index="Region",
    columns="Date",
    values="Estimated Unemployment Rate (%)",
    aggfunc="mean"
)

plt.figure(figsize=(16, 10))
sns.heatmap(pivot, cmap="YlOrRd")
plt.title("Regional Unemployment Rate Heatmap")
plt.xlabel("Date")
plt.ylabel("Region")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "04_regional_heatmap.png", dpi=300)
plt.close()

# 5. Urban/Rural comparison if Area exists
if "Area" in df.columns:
    area_trend = (
        df.groupby(["Date", "Area"])["Estimated Unemployment Rate (%)"]
          .mean()
          .reset_index()
    )
    plt.figure(figsize=(12, 6))
    sns.lineplot(
        data=area_trend,
        x="Date",
        y="Estimated Unemployment Rate (%)",
        hue="Area",
        marker="o"
    )
    plt.title("Urban vs Rural Unemployment Trend")
    plt.xlabel("Date")
    plt.ylabel("Average Unemployment Rate (%)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "05_urban_vs_rural.png", dpi=300)
    plt.close()

# Key numerical insights
peak_row = monthly.loc[monthly["Estimated Unemployment Rate (%)"].idxmax()]
lowest_row = monthly.loc[monthly["Estimated Unemployment Rate (%)"].idxmin()]
highest_region = regional.index[0]

print("\nKEY INSIGHTS")
print(f"Peak monthly average unemployment rate: "
      f"{peak_row['Estimated Unemployment Rate (%)']:.2f}% on {peak_row['Date'].date()}")
print(f"Lowest monthly average unemployment rate: "
      f"{lowest_row['Estimated Unemployment Rate (%)']:.2f}% on {lowest_row['Date'].date()}")
print(f"Highest average regional unemployment rate: {highest_region}")
print(f"Average before COVID: {before_covid:.2f}%")
print(f"Average during Mar-Jun 2020: {covid_period:.2f}%")

print("\nAnalysis completed. Check the 'outputs' folder.")
