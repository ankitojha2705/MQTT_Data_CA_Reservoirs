import paho.mqtt.client as mqtt
import pandas as pd
import json
import time

# MQTT broker settings
broker_address = "broker.hivemq.com"  # Using HiveMQ's public broker
port = 1883  # Standard MQTT port

# MQTT topics mapped to each reservoir
topics = {
    "shasta": "SHASTA/WML",
    "oroville": "OROVILLE/WML",
    "sonoma": "SONOMA/WML"
}

# Connection callback function handles broker connection responses for MQTT v5
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected successfully.")
        # Subscribe to each topic upon successful connection
        for topic in topics.values():
            client.subscribe(topic)
    else:
        print(f"Connection failed with code {rc}: {mqtt.connack_string(rc)}")

# Global dictionary to store aggregated data
daily_aggregates = {}

# Message callback function processes each received MQTT message
def on_message(client, userdata, msg):
    # Decode JSON data from message payload
    data = json.loads(msg.payload.decode())
    date = data['Date']
    taf = data['TAF']
    topic = msg.topic.split('/')[0].lower()  # Extract the reservoir name from the topic

    # Aggregate data by date and reservoir
    if date not in daily_aggregates:
        daily_aggregates[date] = {}
    if topic not in daily_aggregates[date]:
        daily_aggregates[date][topic] = []

    daily_aggregates[date][topic].append(taf)

    # Example of how to print daily summary at end of each day or on a trigger
    print_daily_summary(date)

# Function to print the daily summary for a given date
def print_daily_summary(date):
    if date in daily_aggregates:
        for reservoir, values in daily_aggregates[date].items():
            average_taf = sum(values) / len(values)
            print(f"Date: {date}, Reservoir: {reservoir}, Average TAF: {average_taf}")

# Read CSV file and convert to JSON format
def csv_to_json(filename):
    df = pd.read_csv(filename)
    return df.to_dict(orient='records')

# Initialize the MQTT client with the latest protocol version
client = mqtt.Client(protocol=mqtt.MQTTv5)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
try:
    client.connect(broker_address, port, 60)
except Exception as e:
    print(f"Failed to connect to MQTT broker: {e}")

# Start the network loop in a separate thread
client.loop_start()

# Function to publish data to MQTT topics
def publish_data(data, topic):
    for entry in data:
        message = json.dumps(entry)
        client.publish(topic, message)
        time.sleep(1)  # Simulate time delay between messages

# Load and publish data for each reservoir
try:
    shasta_data = csv_to_json("./Shasta_WML(Sample).csv")
    oroville_data = csv_to_json("./Oroville_WML(Sample).csv")
    sonoma_data = csv_to_json("./Sonoma_WML(Sample).csv")

    publish_data(shasta_data, topics["shasta"])
    publish_data(oroville_data, topics["oroville"])
    publish_data(sonoma_data, topics["sonoma"])
except Exception as e:
    print(f"Error processing files: {e}")

# Allow time for all messages to be sent and processed
time.sleep(20)  # Adjust based on your need

# Stop the loop and disconnect after operations are complete
client.loop_stop()
client.disconnect()
