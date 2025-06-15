#!/bin/sh

# Set target from args
if [ -z "$1" ]; then
  echo "Usage: $0 <target>"
  exit 1
fi
HOST_TARGET=$1

#do in an endless loop
while true; do
  #for every.jpg file in the current directory, tun payload_creator.py
  #usage: payload_creator.py [-h] --image_path IMAGE_PATH --output_path OUTPUT_PATH
    for file in *.jpg; do
        #check if the file exists
        if [ -f "$file" ]; then
        #run the payload_creator.py script with the current file as input
        python3 ./payload_creator.py --image_path "$file" --output_path ./mqtt.payload.icam;
        mosquitto_pub -h $HOST_TARGET -t "i/cam" -f ./mqtt.payload.icam;
        #wait 1 second
        sleep 1;
        fi
    done

  done



