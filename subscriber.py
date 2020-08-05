#--------------------------------------------
#-----Authored and adapted by Nouha Haj salem
#-----Create db ant tables 
#-----Version 1.0
#-----Python Ver : 3.6
#---------------------------------------------

import paho.mqtt.client as mqtt
import influxdb
from storeData import _parse_mqtt_message, _send_sensor_data_to_influxdb
def on_connect(mosq, obj, rc):
    if rc==0:
        print("connected")
        mqttc.subscribe(MQTT_Topic, 0) #Subscribe to all Sensors at Base Topic
    else:
        print("bad connection")

def on_message(client, userdata, msg):
    """The callback for when a PUBLISH message is received from the server."""
    print(msg.topic + ' ' + str(msg.payload))
    sensor_data = _parse_mqtt_message(msg.topic, msg.payload.decode('utf-8'))
    if sensor_data is not None:
        _send_sensor_data_to_influxdb(sensor_data) #Save Data into DB Table

def on_subscribe(mosq, obj, mid, granted_qos):
    pass




# MQTT Settings
MQTT_Broker = "localhost"
MQTT_Port = 1883
Keep_Alive_Interval = 30
MQTT_Topic = "events/serial/#"

mqttc = mqtt.Client()
mqttc.on_message = on_message
mqttc.on_connect = on_connect
mqttc.on_subscribe = on_subscribe

# Connect & subscribe
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
mqttc.subscribe(MQTT_Topic, 0)
mqttc.loop_forever() # Continue the network loop 
