# mqtt_load_test.py
import paho.mqtt.client as mqtt
import time
import threading
import random
import argparse

import csv
from datetime import datetime
from queue import Queue

parser = argparse.ArgumentParser(description="MQTT Load Test")
parser.add_argument('--broker', '-b', required=True, help='MQTT broker IP address')
parser.add_argument('--port', '-p', type=int, default=1883, help='MQTT broker port (default: 1883)')
parser.add_argument('--topic', '-t', default="test/load/", help='MQTT topic base (default: test/load/)')
parser.add_argument('--clients', '-c', type=int, default=50, help='Number of MQTT clients (default: 50)')
parser.add_argument('--msgnum', '-n', type=int, default=100, help='Number of messages per client (default: 100)')
parser.add_argument('--report', '-r', default="mqtt_report.csv", help='Output CSV report file')
args = parser.parse_args()
broker = args.broker
port = args.port
topic_base = args.topic
num_clients = args.clients
messages_per_client = args.msgnum
report_file = args.report

results_queue = Queue()

def run_client(client_id):
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"client_{client_id}")
    result = {
        "client_id": client_id,
        "messages_sent": 0,
        "start_time": time.time(),
        "end_time": None,
        "status": "success",
        "error": ""
    }
    try:
        client.connect(broker, port)
        for i in range(messages_per_client):
            topic = topic_base + str(client_id)
            payload = f"Message {i} from client {client_id}"
            client.publish(topic, payload)
            time.sleep(random.uniform(0.01, 0.1))  # simulate varied frequency
        client.disconnect()
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)
    finally:
        result["end_time"] = time.time()
        results_queue.put(result)

# Test MQTT broker connection before starting load test
test_client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="test_connection")
try:
    test_client.connect(broker, port, keepalive=5)
    test_client.disconnect()
except Exception as e:
    proceed = input(f"[!] Could not connect to MQTT broker at {broker}:{port} ({e}). Continue anyway? [y/N]: ")
    if proceed.lower() != 'y':
        print("[-] Exiting.")
        exit(1)

threads = []
print(f"[*] Starting {num_clients} MQTT clients...")
for i in range(num_clients):
    t = threading.Thread(target=run_client, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("[+] MQTT load test complete.")


results = []
while not results_queue.empty():
    results.append(results_queue.get())

with open(report_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "client_id", "messages_sent", "start_time", "end_time", "duration", "status", "error"
    ])
    writer.writeheader()
    for r in results:
        r["duration"] = round(r["end_time"] - r["start_time"], 2)
        r["start_time"] = datetime.fromtimestamp(r["start_time"]).isoformat()
        r["end_time"] = datetime.fromtimestamp(r["end_time"]).isoformat()
        writer.writerow(r)

# Print summary
success = len([r for r in results if r["status"] == "success"])
fail = len(results) - success
print(f"\n[+] Load test complete. Results saved to '{report_file}'")
print(f"[✓] Successful clients: {success}")
print(f"[✗] Failed clients: {fail}")


