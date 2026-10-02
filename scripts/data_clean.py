import pandas as pd
from pathlib import Path

cities = ["colombo", "jaffna", "kandy", "nuwara_eliya"]

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

dfs = []

for city in cities:
    df = pd.read_csv(RAW_DIR / f"{city}.csv", parse_dates=["date"])
    dfs.append(df)

    print(df.isna().sum())
    print(df["date"].duplicated().sum())
    expected_dates = pd.date_range(start=df["date"].min(), end=df["date"].max(), freq="D")
    missing_dates = expected_dates.difference(df["date"])
    print(len(missing_dates))
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv(DATA_DIR / "all_cities_combined.csv", index=False)

