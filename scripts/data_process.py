import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
from scipy import stats
import itertools

DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "processed"
FIG_DIR = Path(__file__).resolve().parent.parent / "outputs" / "figures"

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
plt.savefig(FIG_DIR / "temperature_seasonality.png", dpi=150)
#plt.show()

rain_wide = monthly.pivot(index='month', columns='city', values='precipitation_sum')
print(rain_wide)

fig, ax = plt.subplots(figsize=(10, 6))

for city in rain_wide.columns:
    ax.plot(rain_wide.index, rain_wide[city], marker='o', label=city)

ax.set_xlabel("Month")
ax.set_ylabel("Rainfall (mm)")
ax.set_title("Monthly Rainfall Seasonality by City")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"])
ax.legend(title="City")
ax.grid(True, alpha=0.3)

# 5. Render and save
plt.tight_layout()
plt.savefig(FIG_DIR / "rainfall_seasonality.png", dpi=150)
#plt.show()

thresholds = {}

for city in df['city'].unique():
    city_data = df[df['city'] == city]
    temp_threshold = city_data['temperature_2m_max'].quantile(0.95)
    rain_threshold = city_data['precipitation_sum'].quantile(0.95)
    thresholds[city] = {'heat': temp_threshold, 'rain': rain_threshold}

print(thresholds)

df["year"] = df["date"].dt.year

df["is_extreme_heat"] = df.apply(lambda row: row["temperature_2m_max"] > thresholds[row["city"]]["heat"], axis=1)
df["is_extreme_rain"] = df.apply(lambda row: row["precipitation_sum"] > thresholds[row["city"]]["rain"], axis=1)

extreme_counts = df.groupby(["city", "year"])[["is_extreme_heat", "is_extreme_rain"]].sum().reset_index()

print(extreme_counts.head())

heat_wide = extreme_counts.pivot(index="year", columns="city", values="is_extreme_heat")

fig, ax = plt.subplots(figsize=(12, 6))
for city in heat_wide.columns:
    ax.plot(heat_wide.index, heat_wide[city], marker="o", markersize=3, label=city)

ax.set_xlabel("Year")
ax.set_ylabel("Number of Extreme Heat Days")
ax.set_title("Extreme Heat Days per Year by City (>95th percentile)")
ax.legend(title="City")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / "extreme_heat_trend.png", dpi=150)
#plt.show()

rain_wide = extreme_counts.pivot(index="year", columns="city", values="is_extreme_rain")

fig, ax = plt.subplots(figsize=(12, 6))
for city in rain_wide.columns:
    ax.plot(rain_wide.index, rain_wide[city], marker="o", markersize=3, label=city)

ax.set_xlabel("Year")
ax.set_ylabel("Number of Extreme Rain Days")
ax.set_title("Extreme Rain Days per Year by City (>95th percentile)")
ax.legend(title="City")
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(FIG_DIR / "extreme_rain_trend.png", dpi=150)
#plt.show()


extreme_counts.to_csv(DATA_DIR / "extreme_day_counts.csv", index=False)

yearly_summary = df.groupby(["city", "year"]).agg({
    "temperature_2m_mean": "mean",
    "precipitation_sum": "sum"
    
}).reset_index()

yearly_summary.to_csv(DATA_DIR / "yearly_summary.csv")

rainfall_summary = yearly_summary.pivot(index="year", columns="city", values="precipitation_sum")

temp_summary = yearly_summary.pivot(index="year", columns="city", values="temperature_2m_mean")

print(rainfall_summary)
print(temp_summary)

def mean_ci(series, confidence=0.95):
    values = series.dropna()
    n = len(values)
    mean = values.mean()
    se = stats.sem(values)
    crit = stats.t.ppf(1-(1 - confidence)/2, df= n-1)
    half_width = crit * se
    return mean, mean - half_width, mean + half_width, half_width

rows = []

for variable, table in [("temperature_2m_mean", temp_summary), ("precipitation_sum", rainfall_summary)]:
    for city in table.columns:
        mean, lower, upper, half_width = mean_ci(table[city])
        rows.append({
            "variable": variable,
            "city": city,
            "mean": mean,
            "ci_low": lower,
            "ci_high": upper,
            "half_width": half_width
        })

city_mean_cis = pd.DataFrame(rows)

city_mean_cis.to_csv(DATA_DIR / "city_mean_cis.csv", index=False)

print(list(itertools.combinations(temp_summary.columns, 2)))