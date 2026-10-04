import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"

df = pd.read_csv(DATA_DIR / "all_cities_combined.csv", parse_dates=["date"])
df['month'] = df['date'].dt.month
print(df)

grouped_avg = df.groupby(['city', 'month'])[['temperature_2m_mean', 'precipitation_sum']].mean().reset_index()

grouped_avg.to_csv(DATA_DIR / "monthly_climatology.csv")

monthly = pd.read_csv(DATA_DIR / "monthly_climatology.csv")

temp_wide = monthly.pivot(index="month", columns="city", values="temperature_2m_mean")

print(temp_wide)

fig, ax = plt.subplots(figsize=(10, 6))

for city in temp_wide.columns:
    ax.plot(temp_wide.index, temp_wide[city], marker="o", label=city)

ax.set_xlabel("Month")
ax.set_ylabel("Average Temperature (°C)")
ax.set_title("Monthly Temperature Seasonality by City")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
ax.legend(title="City")
ax.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig(DATA_DIR / "temperature_seasonality.png", dpi=150)
plt.show()
