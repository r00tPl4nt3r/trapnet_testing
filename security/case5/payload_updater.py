# Reads the .json file and update the ts field with the current timestamp. leave the rest of the payload unchanged. 
# Saves the file with the same name.

import json
import datetime
import argparse
import os
import random

def update_payload(input_path):
    # Define the output path as the same as input path
    output_path = input_path
    # Read the existing JSON payload
    with open(input_path, 'r') as file:
        payload = json.load(file)

    # Update the timestamp field with the current UTC time in ISO 8601 format
    payload['ts'] = datetime.datetime.now(datetime.timezone.utc).isoformat()

    # Save the updated payload to the output path
    with open(output_path, 'w') as file:
        json.dump(payload, file, indent=2)

    print(f"Updated sensor payload saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update the timestamp in a JSON payload.")
    parser.add_argument('--input_path', type=str, required=True, help='Path to the input JSON file')

    args = parser.parse_args()


    # Ensure the input file exists
    if not os.path.exists(args.input_path):
        print(f"Error: Input file {args.input_path} does not exist.")
        exit(1)

    update_payload(args.input_path)