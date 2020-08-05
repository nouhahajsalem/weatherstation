#--------------------------------------------
#-----Authored and adapted by Nouha Haj salem
#-----Create db ant tables 
#-----Version 1.0
#-----Python Ver : 3.6
#---------------------------------------------

import paho.mqtt.client as mqtt
#To import paho mqtt client execute the line commands below:
#pip install paho-mqtt 
import random, threading, json

def on_connect(client, userdata, rc):
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
    print ("Published: " + str(message) + " " + "on MQTT Topic: " + str(topic))
#==============================================================================
#FAKE SENSOR 
#Dummy code used as simulated sensor to publish some random values to MQTT Broker 

def getRandomNumber():
    m = float(10)
    s_rm = 1-(1/m)**2
    return (1-random.uniform(0, s_rm))**.5

#une fois il formate des donnes en format json il les envoie et les pub
def publish_Sensor_Values_to_MQTT():
    threading.Timer(2.0, publish_Sensor_Values_to_MQTT).start()
    global toggle
    if toggle == 0:
        Temperature_Value = float("{0:.2f}".format(random.uniform(10, 100)*getRandomNumber()))
        Temperature_Data = {}
        Temperature_Data['Sensor_ID'] = "Temperature-Sensor1"
        Temperature_Data['Temperature'] = Temperature_Value
        temperature_json_data = json.dumps(Temperature_Data)
        print ("Publishing Temperature Value: " + str(Temperature_Value) + "...")
        publish_To_Topic (MQTT_Topic_Temperature, temperature_json_data)
        toggle = 1
    else:
        #… iden to temperature bloc
        toggle = 0

# MQTT Settings
MQTT_Broker = "localhost"
MQTT_Port = 1883
Keep_Alive_Interval = 30
MQTT_Topic_Temperature = "events/serial/temperature"
#===================================================================
mqttc = mqtt.Client()
mqttc.on_connect = on_connect
mqttc.on_disconnect = on_disconnect
mqttc.on_publish = on_publish
mqttc.connect(MQTT_Broker, int(MQTT_Port), int(Keep_Alive_Interval))
toggle = 0
publish_Sensor_Values_to_MQTT()