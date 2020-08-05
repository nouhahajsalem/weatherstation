#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <../ArduinoJson.h>

const char *ssid = "Nextronic"; // wifi name 
const char *password = "nextronic.ma";  // passwd of wifi 
const char *mqttServer = "192.168.1.140"; // server ip ==> your pc
const int mqttPort = 1883; // by default (port mqtt)
const char *mqttUser = ""; // clear
const char *mqttPassword = ""; // clear
const char* MQTT_Topic_Humidity = "events/serial/humidity";
const char* MQTT_Topic_Temperature = "events/serial/temperature";

WiFiClient espClient;
PubSubClient client(espClient);
StaticJsonDocument<512> action;
void callback(char *topic, byte *payload, unsigned int length)
{

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  deserializeJson(action, payload);

  serializeJson(action, Serial);
  Serial.println();
  Serial.println("-----------------------");
}

void setup()
{

  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected())
  {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword))
    {

      Serial.println("connected");
    }
    else
    {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);
    }
  }
  client.subscribe("action/as8d46a5se8");
  //client.publish("events", "{\"serial\":\"as8d46a5se8\",\"count\":156}");
}
char output[1024];
void loop()
{
  DynamicJsonDocument doc(1024);
  doc["serial"] = "Serial";
  doc["temp_in"] = 874984;
  doc["temp_out"] = '0';
  doc["Humidity"] = '0';
  doc["Pressure"] = '0';
  doc["windspeed"] = '0';
  doc["precipitation"] = '0';
  

  serializeJson(doc, output);

  client.publish("events", output);
  delay(1000);
  Serial.println("Message send ");
  client.loop();
}
