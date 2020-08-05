#--------------------------------------------
#-----Authored and adapted by Nouha Haj salem
#-----Create db ant tables 
#-----Version 1.0
#-----Python Ver : 3.6
#---------------------------------------------

import paho.mqtt.client as mqtt
import random, threading, json

def on_conect(client, userdata, rc):
    if rc != 0:
        pass
        print ("Unable to connect to MQTT Broker...")
    else:
        print ("Connected with MQTT Broker: " + str(MQTT_Broker))

def on_publish(client, userdata, mid):
    pass

def on_disconnect(client, userdata, rc):
    if rc !=0:
        pass

def publish_To_Topic(topic, message):
    mqttc.publish(topic,message)
    print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic)+ "")

# Code used as simulated Sensor to publish some random values to MQTT Broker

def getRandomNumber():
    m = float(10)
    s_rm = 1-(1/m)**2
    return (1-random.uniform(0, s_rm))**.5

def publish_Sensor_Values_to_MQTT():
    threading.Timer(2.0, publish_Sensor_Values_to_MQTT).start()
    global toggle
    if toggle == 0:
        Humidity_Value = float("{0:.2f}".format(random.uniform(10, 100)*getRandomNumber()))
        Humidity_Data = {}
        Humidity_Data['Sensor_ID'] = "Humidity-Sensor1"
        Humidity_Data['Humidity'] = Humidity_Value
        humidity_json_data = json.dumps(Humidity_Data)
        print ("Publishing Humidity Value: " + str(Humidity_Value) + "...")
        publish_To_Topic (MQTT_Topic_Humidity, humidity_json_data)
        toggle = 1
    else:
        #… iden to humidity bloc
        toggle = 0

# MQTT Settings
MQTT_Broker = "localhost"
MQTT_Port = 1883
Keep_Alive_Interval = 30
MQTT_Topic_Humidity = "events/serial/humidity"

mqttc = mqtt.Client()
mqttc.on_connect = on_conect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
toggle = 0
publish_Sensor_Values_to_MQTT()