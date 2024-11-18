# California Reservoirs MQTT Data Aggregator

## Project Overview
This project demonstrates the use of MQTT to collect and aggregate Water Mark Levels (TAF) from various reservoirs in California, focusing on real-time data handling and processing. The system subscribes to specific MQTT topics designated for each reservoir and calculates daily average TAF values to assist in water resource management.

## Features
- **MQTT Data Collection**: Utilizes MQTT protocol to collect real-time TAF data from multiple reservoirs.
- **Data Aggregation**: Aggregates daily water mark levels to compute average values.
- **Reporting**: Generates reports summarizing the aggregated data, which are crucial for analyzing water resource trends and planning.

## Technology Stack
- **MQTT**: For messaging and data transmission.
- **Python**: Scripting language used to write the subscriber and publisher scripts.
- **Paho-MQTT**: Python library that provides client classes for communicating with MQTT brokers.

## Getting Started

### Prerequisites
- Python 3.8 or higher
- Paho-MQTT Python library

  You can install the necessary library using pip:
  ```bash
  pip install paho-mqtt
