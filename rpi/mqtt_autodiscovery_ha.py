"""
* -----------------------------------------------------------------------------------
* Last update :  16/06/2024
* Arrosage Automatique
* Script à executer pour créer automatiquement les entités mqtt dans homeassistant (autodiscovery actif dans ha)
* => relancer si modifications et/ou ajouts
* -----------------------------------------------------------------------------------
"""

import paho.mqtt.client as mqtt
import json
import time

IP_MQTT_BROKER = '192.168.1.125'
USER_MQTT = 'nicolas'
PASSWORD_MQTT = 'lkmjkgfdfrtpcv'
PORT_MQTT = 1883

f = open("Raspberry/json/mqtt_autodiscovery_ha.json")
config_autodiscovery = json.load(f)
f.close()

client = mqtt.Client(protocol = mqtt.MQTTv5)
#client = mqtt.Client("arrosage") #create new instance
client.username_pw_set(username=USER_MQTT,password=PASSWORD_MQTT) #set user and password
client.connect(host=IP_MQTT_BROKER,port=PORT_MQTT) #connect to broker

for entity in config_autodiscovery['entities']:
    client.publish(entity['topic'],entity['payload'],retain=True)
    print(entity['topic'])
    time.sleep(0.5)

client.disconnect() #disconnect
