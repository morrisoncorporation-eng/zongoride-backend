#!/bin/sh

# This script runs in an infinite loop to simulate IoT devices publishing data.

# Give the Mosquitto broker a moment to start up
echo "Waiting for Mosquitto broker to be ready..."
sleep 5 

echo "Starting data publication loop..."
while :
do
  # --- Scooter 1 ---
  # Generate slightly randomized coordinates around a central point
  LAT1=$(echo "40.7484 + ( $RANDOM % 100 - 50 ) / 10000.0" | bc)
  LON1=$(echo "-73.9857 + ( $RANDOM % 100 - 50 ) / 10000.0" | bc)
  
  # Construct the JSON payload
  PAYLOAD1="{\"latitude\": $LAT1, \"longitude\": $LON1}"
  
  # Publish to the location topic for scooter 1, using the correct hostname 'mqtt-broker'
  mosquitto_pub -h mqtt-broker -p 1883 -t "scooters/1/location" -m "$PAYLOAD1"
  echo "Published for Scooter 1: $PAYLOAD1"

  # --- Scooter 2 ---
  LAT2=$(echo "40.7580 + ( $RANDOM % 100 - 50 ) / 10000.0" | bc)
  LON2=$(echo "-73.9855 + ( $RANDOM % 100 - 50 ) / 10000.0" | bc)
  PAYLOAD2="{\"latitude\": $LAT2, \"longitude\": $LON2}"
  mosquitto_pub -h mqtt-broker -p 1883 -t "scooters/2/location" -m "$PAYLOAD2"
  echo "Published for Scooter 2: $PAYLOAD2"

  # Wait for 10 seconds before the next loop
  sleep 10
done
