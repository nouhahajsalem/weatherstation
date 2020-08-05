#--------------------------------------------
#-----Authored and adapted by Nouha Haj salem
#-----Create db ant tables 
#-----Version 1.0
#-----Python Ver : 3.6
#---------------------------------------------
import json
import re
from typing import NamedTuple
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
from publisherTemperature import publish_Sensor_Values_to_MQTT
from publisherHumidity import publish_Sensor_Values_to_MQTT

# Set envirenments variables 
INFLUXDB_USER = 'mqtt'
INFLUXDB_PASSWORD = 'mqtt'
INFLUXDB_DATABASE = 'weatherStationDB'

MQTT_ADDRESS = '192.168.0.8'
MQTT_TOPIC = 'events/serial/#'
MQTT_REGEX = 'events/([^/]+)/([^/]+)'

influxdb_client = InfluxDBClient('localhost', 8086, 'mqtt', 'mqtt', 'weatherStationDB')

class SensorData(NamedTuple):
    measurement: str
    value: float

def _send_sensor_data_to_influxdb(sensor_data):
    humidity_body = [
            {
                "measurement": "humidity",
                "tags": {
                    "host": "server01"
                },
                "fields": {
                    "name": "Humidity-Sensor1",
                    "value": sensor_data.value,
                }
            }
        ]
    temperature_body = [
            {
                "measurement": "temperature",
                "tags": {
                    "host": "server01"
                },
                "fields": {
                    "name": "temperature-Sensor1",
                    "value": sensor_data.value,
                }
            }
        ]
    influxdb_client.write_points(humidity_body)
    influxdb_client.write_points(temperature_body)
    result = influxdb_client.query('select last(value) as "humidity" from humidity;')
    print("Humidity : {0}".format(result))
    result = influxdb_client.query('select last(value) as "temperature" from temperature;')
    print("Temperature : {0}".format(result))



def _parse_mqtt_message(topic, payload):
    match = re.match(MQTT_REGEX, topic)
    if match:
        measurement = match.Temperature_Value
        if measurement == 'status':
            return None
        return SensorData(measurement, float(payload))
    elif match:
        measurement = match.Humidity_Value
        if measurement == 'status':
            return None
        return SensorData(measurement, float(payload))

    else:
        return None


