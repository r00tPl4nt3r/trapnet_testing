import os
import pandas as pd
import re

folder = "./"
combined = []

for filename in os.listdir(folder):
    if filename.endswith(".csv") and "pi_mqtt_resultsc" in filename:
        match = re.search(r"c(\d+)n(\d+)", filename)
        if match:
            clients = int(match.group(1))
            messages = int(match.group(2))
            
            df = pd.read_csv(os.path.join(folder, filename))
            df["clients"] = clients
            df["messages_per_client"] = messages
            df["scenario"] = f"{clients}c_{messages}m"
            combined.append(df)

# Save all in one file
result = pd.concat(combined, ignore_index=True)
result.to_csv("pi_mqtt_combined_results.csv", index=False)
