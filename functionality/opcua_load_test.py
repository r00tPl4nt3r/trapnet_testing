# opcua_load_test.py
import argparse
import time
import random
from datetime import datetime
import threading
from queue import Queue
from opcua import Client, ua
import csv

FIXED_VARIABLE = "ns=3;s=\"gtyp_SSC\".\"di_Pos_Park_Horizontal\""
FIXED_VALUE = 3001


parser = argparse.ArgumentParser(description="OPC UA Load Test")
parser.add_argument('--server', '-s', required=True, help='OPC UA server URL')
parser.add_argument('--clients', '-c', type=int, default=50, help='Number of OPC UA clients (default: 50)')
parser.add_argument('--msgnum', '-n', type=int, default=100, help='Number of messages per client (default: 100)')
parser.add_argument('--report', '-r', default="opcua_report.csv", help='Output CSV report file')
parser.add_argument('--nodeID', '-id', default=FIXED_VARIABLE, type=str, help='OPC UA variable node ID to write to')  
parser.add_argument('--nodeValue', '-v', type=int, default=FIXED_VALUE, help='Value to write to the OPC UA variable (default: 3001)')

args = parser.parse_args()
server_url = args.server
num_clients = args.clients
messages_per_client = args.msgnum
report_file = args.report
node_id = args.nodeID
payload = args.nodeValue
results_queue = Queue()

def run_client(client_id):
    client = Client(server_url)
    result = {
        "client_id": client_id,
        "messages_sent": 0,
        "messages_failed": 0,
        "start_time": time.time(),
        "end_time": None,
        "status": "success",
        "error": ""
    }
    try:
        client.connect()
        client.load_type_definitions()
        node = client.get_node(node_id)
        latencies = []
        successful_confirms = 0
        for i in range(messages_per_client):
            try:
                newvalue = ua.DataValue(ua.Variant(payload, ua.VariantType.Int32))
                newvalue.ServerTimestamp = datetime.now()
                newvalue.SourceTimestamp = datetime.now()

                start = time.perf_counter()
                node.set_value(newvalue)
                confirmed_value = node.get_value()
                end = time.perf_counter()

                if confirmed_value == payload:
                    latencies.append(end - start)
                    result["messages_sent"] += 1
                    successful_confirms += 1

                else:
                    result["messages_failed"] += 1
                    result["error"] = f"Write mismatch: expected {payload}, got {confirmed_value}"

            except Exception as e:
                result["messages_failed"] += 1
                result["error"] = str(e)

            time.sleep(random.uniform(0.01, 0.1))

        time.sleep(0.2)
    except Exception as e:
        result["status"] = "error"
        result["error"] = str(e)

    finally:
        result["end_time"] = time.time()
        result["avg_latency_ms"] = round(1000 * sum(latencies) / len(latencies), 2) if latencies else 0
        result["confirmed_writes"] = successful_confirms
        try:
            if client.uaclient._uasocket and client.uaclient._uasocket._socket:
                client.disconnect()
        except Exception as e:
            result["status"] = "error"
            result["error"] += f" | Disconnect failed: {e}"


        results_queue.put(result)

def main():
    clients = []
    for i in range(num_clients):
        client_thread = threading.Thread(target=run_client, args=(i,))
        clients.append(client_thread)
        client_thread.start()

    for client_thread in clients:
        client_thread.join()

    # Collect results from queue
    results = []
    while not results_queue.empty():
        results.append(results_queue.get())

    # Write results to CSV
    with open(report_file, 'w', newline='') as csvfile:
        fieldnames = [
        "client_id", "messages_sent", "messages_failed",
        "confirmed_writes", "avg_latency_ms",
        "start_time", "end_time", "status", "error"
        ]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for r in results:
            writer.writerow(r)

   # Print summary
    success = len([r for r in results if r["status"] == "success"])
    fail = len(results) - success
    print(f"\n[+] Load test complete. Results saved to '{report_file}'")
    print(f"[✓] Successful clients: {success}")
    print(f"[✗] Failed clients: {fail}")


if __name__ == "__main__":
    main()  







