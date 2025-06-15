import json
import datetime
import random

# Generate a timezone-aware ISO timestamp in UTC
timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()

# Construct BME680-style payload with realistic mock values
sensor_payload = {
    "aq": random.randint(0, 50),                                      # Air Quality Index
    "gr": float(random.randint(500000, 1000000)),                     # Gas Resistance (Ohms)
    "h": round(random.uniform(20.0, 40.0), 1),                         # Humidity (simple)
    "iaq": round(random.uniform(50.0, 150.0), 1),                      # Indoor Air Quality Score
    "p": round(random.uniform(975.0, 1020.0), 14),                     # Pressure (hPa)
    "rh": round(random.uniform(20.0, 60.0), 2),                        # Relative Humidity (%)
    "rt": round(random.uniform(20.0, 30.0), 15),                       # Raw Temperature (°C)
    "t": round(random.uniform(20.0, 25.0), 7),                         # Temperature (°C)
    "ts": timestamp
}

# Save to JSON file
output_path = '/mnt/data/bme680_latest_output.json'
with open(output_path, 'w') as f:
    json.dump(sensor_payload, f, indent=2)

print(f"Updated sensor payload saved to: {output_path}")
