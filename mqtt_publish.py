"""
* -----------------------------------------------------------------------------------
* Last update :  23/10/2024
* Arrosage Automatique
* Tache de publication des données vers le brocker mqtt (toutes les 10 secondes)
* -----------------------------------------------------------------------------------
"""

import paho.mqtt.client as mqtt
import yaml
import json
from sqlalchemy import create_engine,text
import logging
import time
from function import ConfigLogging,GetDayTime,DbClose,DbConnect,AddMqttQueue

if __name__ == '__main__':
	#---------------------------------------
	# parametres
	import config as config
	
	#--------------------------------------
	#initialise logging config
	actual_day = GetDayTime(0)
	logger = logging.getLogger(__name__)#.addHandler(logging.NullHandler())
	#logfile = "log/mqtt_subscribe"+str(actual_day.day)+"_"+str(actual_day.month)+"_" +str(actual_day.year)+".txt"
	logfile = "log/mqtt_publish.txt"
	ConfigLogging(logger,logfile,config.LOG_LEVEL_STREAM,config.LOG_LEVEL_FILE,True)
	
	cpt=0
	cpt_error=0

	while True:
		cpt+=1
		try:
			engine,connection = DbConnect(logger)
			try:
				sql = 'select * from Mqtt_Queue where Published=0 order by date_ajout asc'
				result = connection.execute(text(sql))
				rows = result.all()
				nbrows = len(rows)
				if nbrows>0:
					client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,"arrosage_pub_loop")
					client.username_pw_set(username=config.USER_MQTT,password=config.PASSWORD_MQTT)
					client.connect(host=config.IP_MQTT_BROKER,port=config.PORT_MQTT)
					for row in rows:
						client.publish(row.topic,row.payload,retain=row.retain)	#publish data to the specified topic
						logger.debug(f'Mqtt => Topic : {row.topic} => Payload : {row.payload}')
						sql = f'Update Mqtt_Queue set published=1,date_publish=now() where id_mqtt_queue={row.id_mqtt_queue}'
						connection.execute(text(sql))
						connection.commit()
						#print(sql)
						time.sleep(0.2)
					client.publish('ha/arrosage/status/loop_mqtt_publish',str(cpt),retain=True,qos=0)
					client.publish('ha/arrosage/status/loop_mqtt_publish_erreur',str(cpt_error),retain=True,qos=0)
					client.disconnect() #disconnect
			except Exception as e:
				cpt_error+=1
				logger.exception(f'Erreur mqtt publish msg : {e}')
		except Exception as e:
			cpt_error+=1
			logger.exception(f'Erreur connexion bdd mqtt_publish.py msg : {e}')
		finally:
			try:
				DbClose(engine,connection,logger)
			except Exception as e:
				cpt_error+=1
				logger.exception(f'Erreur Dbclose Boucle Publish mqtt msg : {e}')
		logger.debug('Boucle Mqtt Publish : '+str(cpt))
		logger.debug("==============     FIN LOOP          ==============")
		time.sleep(2)