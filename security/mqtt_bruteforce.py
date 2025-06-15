import paho.mqtt.client as mqtt
import json
from IPython import display
from base64 import b64decode
import time
import random
import datetime
import logging

port = 1883
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("192.168.0.6", port=1883)

