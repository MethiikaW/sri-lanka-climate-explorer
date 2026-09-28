import time
from pathlib import Path

import pandas as pd
import requests

URL = "https://archive-api.open-meteo.com/v1/archive"

# Project root = the folder above scripts/
RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

CITIES = {
    "colombo": (6.93, 79.85),
    "kandy": (7.29, 80.63),
    "jaffna": (9.66, 80.02),
    "nuwara_eliya": (6.97, 80.77),
}

DAILY_VARS = "temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum"


def fetch_city(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": "1995-01-01",
        "end_date": "2025-12-31",
        "daily": DAILY_VARS,
        "timezone": "Asia/Colombo",
    }
    response = requests.get(URL, params=params, timeout=60)
    response.raise_for_status()
    return response.json()


for city, (lat, lon) in CITIES.items():
    out_path = RAW_DIR / f"{city}.csv"

    if out_path.exists():
        print(f"{city}: already downloaded, skipping")
        continue

    print(f"{city}: fetching...")
    data = fetch_city(lat, lon)

    df = pd.DataFrame(data["daily"])
    df = df.rename(columns={"time": "date"})
    df["city"] = city

    df.to_csv(out_path, index=False)
    print(f"{city}: saved {len(df)} rows to {out_path}")

    time.sleep(5)  # be polite to the free API