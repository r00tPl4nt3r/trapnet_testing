# mqtt_load_test.py
import paho.mqtt.client as mqtt
import time
import threading
import random
import argparse

parser = argparse.ArgumentParser(description="MQTT Load Test")
parser.add_argument('--broker', '-b', required=True, help='MQTT broker IP address')
parser.add_argument('--port', '-p', type=int, default=1883, help='MQTT broker port (default: 1883)')
parser.add_argument('--topic', '-t', default="test/load/", help='MQTT topic base (default: test/load/)')
parser.add_argument('--clients', '-c', type=int, default=50, help='Number of MQTT clients (default: 50)')
parser.add_argument('--msgnum', '-n', type=int, default=100, help='Number of messages per client (default: 100)')
args = parser.parse_args()
broker = args.broker
port = args.port
topic_base = args.topic
num_clients = args.clients
messages_per_client = args.msgnum

def run_client(client_id):
    client = mqtt.Client(f"client_{client_id}")
    client.connect(broker, port)
    for i in range(messages_per_client):
        topic = topic_base + str(client_id)
        payload = f"Message {i} from client {client_id}"
        client.publish(topic, payload)
        time.sleep(random.uniform(0.01, 0.1))  # simulate varied frequency
    client.disconnect()


# Test MQTT broker connection before starting load test
test_client = mqtt.Client("test_connection")
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

