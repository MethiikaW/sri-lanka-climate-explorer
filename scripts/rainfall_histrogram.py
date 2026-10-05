import pandas as pd
import matplotlib.pyplot as plt
from  scipy.stats import skew
from pathlib import Path



PROCESSED_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
FIG_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"

combined = pd.read_csv(PROCESSED_DIR/ 'all_cities_combined.csv', parse_dates=['date'])
rainfall = combined["precipitation_sum"]

rainfall = rainfall.dropna()

fig, ax = plt.subplots(figsize=(10,6))

ax.hist(rainfall, bins=50)

ax.set_xlabel("Daily Rainfall (mm)")
ax.set_ylabel("Number of Days")
ax.set_title("Distribution of Daily Rainfall — All Cities, 1995–2025")
ax.set_yscale("log")

plt.tight_layout()
plt.savefig(FIG_DIR / "rainfall_distribution.png", dpi=150)
plt.show()

rainfall_skew = skew(rainfall)
print(f"skewness of daily rainfall: {rainfall_skew:.2f}")
