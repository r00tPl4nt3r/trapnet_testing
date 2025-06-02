# mqtt_load_test.py
import paho.mqtt.client as mqtt
import time
import threading
import random
import argparse

parser = argparse.ArgumentParser(description="MQTT Load Test")
parser.add_argument('--broker', '-b', required=True, help='MQTT broker IP address')
args = parser.parse_args()
broker = args.broker
port = 1883
topic_base = "test/load/"
num_clients = 50
messages_per_client = 100

def run_client(client_id):
    client = mqtt.Client(f"client_{client_id}")
    client.connect(broker, port)
    for i in range(messages_per_client):
        topic = topic_base + str(client_id)
        payload = f"Message {i} from client {client_id}"
        client.publish(topic, payload)
        time.sleep(random.uniform(0.01, 0.1))  # simulate varied frequency
    client.disconnect()

threads = []
print(f"[*] Starting {num_clients} MQTT clients...")
for i in range(num_clients):
    t = threading.Thread(target=run_client, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("[+] MQTT load test complete.")

