"""
* -----------------------------------------------------------------------------------
* Last update :  23/10/2024
* Arrosage Automatique
* Tache de récupération des données depuis mqtt pour maj la bdd (topics update from mosquito brocker)
* lister les topics + boucle sur txt / yaml / json ?
* LogDatabase too slow ?
* -----------------------------------------------------------------------------------
"""

import paho.mqtt.client as mqtt
import yaml
import json
from sqlalchemy import create_engine 
import logging
import time
from function import ConfigLogging,GetDayTime,RestartRpi,UpdateData,LogDatabase,LaunchTestRelais,DbClose,DbConnect

if __name__ == '__main__':
	#---------------------------------------
	# parametres
	import config as config
 
	#--------------------------------------
	#initialise logging config
	actual_day = GetDayTime(0)
	logger = logging.getLogger(__name__)#.addHandler(logging.NullHandler())
	#logfile = "log/mqtt_subscribe"+str(actual_day.day)+"_"+str(actual_day.month)+"_" +str(actual_day.year)+".txt"
	logfile = "log/mqtt_subscribe.txt"
	ConfigLogging(logger,logfile,config.LOG_LEVEL_STREAM,'NOTSET',True)

	#mqtt_logger = logging.getLogger("MqttCon")

	f = open(config.FILE_TOPIC_MQTT)
	topics = json.load(f)
	f.close()

	list_topics = []
	for subpart in topics:
		for type_topic, listtopic in subpart.items():
			for value in listtopic:
				logger.debug("partie {0} topics : {1} bdd : {2} table : {3}".format(type_topic,value['topic'],value['field'],value['table']))
				list_topics.append(tuple([type_topic,config.PREFIX_MQTT+"/"+config.DEVICE_MQTT+"/"+value['topic'],value['field'],value['table']]))
	logger.debug("Topic settings :")

	#subscribe_topics = []
	#for type_topic,topic_name,field_name,table_name in list_topics:
	#	topic = topic_name
	#	subscribe_topics.append(topic)
	#logger.debug("Topics to subscribe :")
	#logger.debug(subscribe_topics)
	#for topic in subscribe_topics:
	#	logger.debug(topic)

	# Fonction appelée lorsque le client reçoit un message d'un sujet auquel il est abonné
	# prevoir un publish sur topic state pour 2025 apres reception du susbscribe 
	def on_message(client, userdata, message):
		#msg_payload = str(message.payload.decode("utf-8")).strip()
		#msg_topic = message.topic
		#logger.info(f'topic : {msg_topic} value :{msg_payload}')
		try:
			engine,connection = DbConnect(logger)
			try:
				msg_payload = str(message.payload.decode("utf-8")).strip()
				if msg_payload != '':
					msg_topic = message.topic
					#if msg_topic[:19] != 'ha/arrosage/status/' and msg_topic[:13] != 'ha/arrosage/Z' and msg_topic[:13] != 'ha/arrosage/S':
						#logger.info(f'topic : {msg_topic} value :{msg_payload}')
						#pass
					#print("Message reçu sur le sujet '" + message.topic + "': ", str(message.payload.decode("utf-8")))
					if msg_topic in ["ha/arrosage/action/restart","ha/arrosage/action/test_relais"] :
						logger.debug(msg_payload)
						LogDatabase(msg_topic.replace('ha/arrosage/',''),msg_payload,'','','mqtt',connection,logger)
						if msg_payload == 'test_relais':
							LaunchTestRelais(logger)
						else:
							RestartRpi(logger)
					else:
						for type_topic,topic_name,field_name,table_name in list_topics:
							if msg_topic==topic_name and type_topic[:1] in ['Z','S']:
								field_filter = "sv" if type_topic[:1]=='Z' else "Seq"
								LogDatabase(msg_topic.replace('ha/arrosage/',''),msg_payload,table_name,field_name,'mqtt',connection,logger)
								UpdateData(table_name,field_name,msg_payload,field_filter,type_topic,type_topic[:1],connection,logger)
								logger.debug(f'update topic : {topic_name} value : {msg_payload}')
							else:
								if msg_topic==topic_name and type_topic == 'param':
									LogDatabase(msg_topic.replace('ha/arrosage/',''),msg_payload,table_name,field_name,'mqtt',connection,logger)
									UpdateData(table_name,field_name,msg_payload,'','',type_topic[:1],connection,logger)
									logger.debug(f'update topic : {topic_name} value : {msg_payload}')
				else:
					logger.warning(f'Payload vide topic : {msg_topic}')
			except Exception as e:
				logger.exception(f'Erreur on_message mqtt_subscibre msg : {e}')
		except Exception as e:
			logger.exception(f'Erreur connexion bdd mqtt_subscibre.py msg : {e}')
		finally:
			try:
				DbClose(engine,connection,logger)
			except Exception as e:
				logger.exception(f'Erreur Dbclose Boucle Json msg : {e}')


	def on_disconnect(client, userdata,  rc):
		logger.warning(f"Disconnected from MQTT broker ! return code rc : {rc}")
		# Tenter de se reconnecter
		while rc != 0:
			logger.warning(f"Attempt to reconnect in 15 seconds ! code rc : {rc}")
			time.sleep(15)
			try:
				client.reconnect()
			except:
				logger.warning(f"Reconnection problem ! code rc : {rc}")
				pass

	def on_log(client, userdata, level, buf):
		#logger.info(f"SYSTEM: {buf}")
		pass

	def on_connect(client, userdata, flags, rc, properties=None):
		if rc==0:
			logger.info("Connected to MQTT Broker")
		else:
			logger.error(f"Connection failed to MQTT Broker RC : {rc}")

	client = mqtt.Client(client_id="arrosage_subscriber", clean_session=False, userdata=None, transport="tcp")
	#client = mqtt.Client()
	client.username_pw_set(config.USER_MQTT, config.PASSWORD_MQTT)
	#client.connect(config.IP_MQTT_BROKER,port = config.PORT_MQTT,keepalive=240)
	client.connect(config.IP_MQTT_BROKER,port = config.PORT_MQTT)
	#client.subscribe(subscribe_topics)
	client.subscribe("ha/arrosage/#",qos=1)
	client.on_connect = on_connect
	client.on_message = on_message
	#client.on_log = on_log
	client.on_disconnect = on_disconnect
	client.loop_forever(retry_first_connection=True)
 	#client.reconnect_delay_set(60,60)
	client.reconnect