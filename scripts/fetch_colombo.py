import requests

URL = "https://archive-api.open-meteo.com/v1/archive"

params = {
    "latitude": 6.93,
    "longitude": 79.85,
    "start_date": "1995-01-01",
    "end_date": "2025-12-31",
    "daily": "temperature_2m_mean,temperature_2m_max,temperature_2m_min,precipitation_sum",
    "timezone": "Asia/Colombo",
}

response = requests.get(URL, params=params, timeout=60)
response.raise_for_status()
data = response.json()

print("Top-level keys:", list(data.keys()))
print("Units:", data["daily_units"])
print("Daily keys:", list(data["daily"].keys()))
print("Number of days:", len(data["daily"]["time"]))
print("First 3 dates:", data["daily"]["time"][:3])
print("First 3 mean temps:", data["daily"]["temperature_2m_mean"][:3])
print("First 3 rainfall values:", data["daily"]["precipitation_sum"][:3])