#!/bin/sh
#do in an endless loop
while true; do
  #publish the payload to the MQTT broker
  mosquitto_pub -h 192.168.183.7  -t "i/cam" -f ./mqtt.payload.flag1;
  #wait 1 second
  sleep 1;
  mosquitto_pub -h 192.168.183.7  -t "i/cam" -f ./mqtt.payload.flag1;
  #wait 1 second
  sleep 1;
  mosquitto_pub -h 192.168.183.7  -t "i/cam" -f ./mqtt.payload.flag1;
  #wait 1 second
  sleep 1;
  mosquitto_pub -h 192.168.183.7  -t "i/cam" -f ./mqtt.payload.flag1;
  #wait 1 second
  sleep 1;

  done



