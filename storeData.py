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

# def _send_sensor_data_to_influxdb(sensor_data):
def _send_sensor_data_to_influxdb(topic, payload):
    humidity_body = [
        {
            "measurement": "humidity",
            "tags": {
                "host": "server01"
            },
            "fields": {
                "name": "Humidity-Sensor1",
                "value": payload,
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
                "value": payload,
            }
        }
    ]
    print(topic)
    # condition on topic to  write measurement
    if ("humidity" in topic):
        influxdb_client.write_points(humidity_body)
        result = influxdb_client.query('select last(value) as "humidity" from humidity;')
        print("Humidity : {0}".format(result))
    elif ("temperature" in topic):
        influxdb_client.write_points(temperature_body)
        result = influxdb_client.query('select last(value) as "temperature" from temperature;')
        print("Temperature : {0}".format(result))

def _parse_mqtt_message(topic, payload):
    print('machakil')
    match = re.match(MQTT_REGEX, topic)
    if match:
        print('case 1')
        measurement = match.temperature
        if measurement == 'status':
            print('what is this')
            return None
        print('what is this')
        return SensorData(measurement, float(payload))
    elif match:
        print('case 2')
        measurement = match.Humidity_Value
        if measurement == 'status':
            return None
        return SensorData(measurement, float(payload))
    else:
        print('case 3')
        return None