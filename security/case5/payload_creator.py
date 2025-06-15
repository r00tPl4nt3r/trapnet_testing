import base64
import json
import argparse

from datetime import datetime

# read input and output paths from the args
parser = argparse.ArgumentParser(description="Create a JSON payload with an image.")
parser.add_argument('--image_path', type=str, required=True, help='Path to the image file')
parser.add_argument('--output_path', type=str, required=True, help='Path to save the output JSON file')


args = parser.parse_args()
image_path = args.image_path
output_path = args.output_path

# Read and encode the image
with open(image_path, "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    image_data = f"data:image/png;base64,{encoded_string}"

# Get current UTC timestamp in ISO 8601 format
timestamp = datetime.datetime.now(datetime.UTC)

# Create the payload
payload = {
    "data": image_data,
    "ts": timestamp
}

# Save JSON to a file
with open(output_path, 'w') as json_file:
    json.dump(payload, json_file, indent=2)

print(f"JSON payload saved to: {output_path}")
