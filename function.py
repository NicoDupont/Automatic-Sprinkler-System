"""
* -----------------------------------------------------------------------------------
* Last update :  15/12/2024
* Arrosage Automatique / IrriPi
* project function catalog
* -----------------------------------------------------------------------------------
"""

from sqlalchemy import create_engine
import ntplib
import datetime,time
import pandas as pd
import os
import json
import yaml
import RPi.GPIO as GPIO
import paho.mqtt.client as mqtt
import logging
import requests
from logging.handlers import TimedRotatingFileHandler
from subprocess import check_output,call,run,PIPE
import socket
from platform import system,python_version,uname
from gpiozero import CPUTemperature,LoadAverage,DiskUsage
from uptime import uptime
from sqlalchemy import text
import psutil

import config as config

def ConfigLogging(logger,logfile,stream_level,file_level,rotating):
	logger_levels = {
	'ERROR' : logging.ERROR,
	'INFO' : logging.INFO,
	'DEBUG' : logging.DEBUG,
	'NOTSET' : logging.NOTSET,
	'WARNING' : logging.WARNING,
	'CRITICAL' : logging.CRITICAL
	}
	logger.setLevel(logger_levels[stream_level])
	# Format for our loglines
	#formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(funcName)s - %(message)s")
	formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s")
	# Setup console logging
	ch = logging.StreamHandler()
	ch.setLevel(logger_levels[stream_level])
	ch.setFormatter(formatter)
	logger.addHandler(ch)
	# Setup file logging as well
	if rotating:
		fh = TimedRotatingFileHandler(logfile,encoding='utf-8',when='d',backupCount=10,interval=1)
	else:
		fh = logging.FileHandler(logfile,encoding='utf-8')
	fh.setLevel(logger_levels[file_level])
	fh.setFormatter(formatter)
	logger.addHandler(fh)

def DbConnect(logger) -> tuple:
	try:
		engine = create_engine('mariadb+mariadbconnector://{0}:{1}@{2}/{3}'.format(config.USER_BDD,config.PASSWORD_BDD,config.IP_BDD_SERVER,config.NAME_DATABASE),
					pool_recycle=500,
					pool_size=5,
					max_overflow=5).execution_options(autocommit=True)
		connection = engine.connect()
	except Exception:
		logger.exception('Problem connection to mariadb')
		connection = None
		engine = None
	finally:
		return [engine,connection]



def DbClose(engine, connection, logger) -> None:
	try:
		connection.close()
		engine.dispose()
	except Exception:
		logger.exception('Problem deconnection mariadb')

# simple test
def IsAbove(value,threshold) -> bool:
	return True if value > threshold else False

def IsBelow(value,threshold) -> bool:
	return True if value < threshold else False

# test yes or no / true or false
def IsTof(value) -> bool:
	return True if value == 1 or value == True else False

# unit test if gpio is high or low
def IsHst(gpio) -> bool:
	test = GPIO.input(gpio)
	return False if test == 0 else True

# start irrigation for the solenoid valve connected to this gpio
def CloseRelay(gpio,logger) -> None:
	GPIO.output(gpio, GPIO.LOW)
	logger.debug(f'Close relay : {gpio}')

# stop irrigation for the solenoid valve connected to this gpio
def OpenRelay(gpio,logger) -> None:
	GPIO.output(gpio, GPIO.HIGH)
	logger.debug(f'Open relay : {gpio}')

#number is even or not
def IsEven(x) -> bool:
	return True if x % 2 == 0 else False
#number is odd or not
def IsOdd(x) -> bool:
	return False if x % 2 == 0 else True

# determines if a solenoid valve/zone is within its programming range
def IsProgrammed(sv,start_time,end_time,datehour,even,odd,monday,tuesday,wednesday,thursday,friday,saturday,sunday,test,logger) -> bool:
	try:
		prog = False
		planned = False
		weekday = datehour.isoweekday()
		yearday = datehour.timetuple().tm_yday #test on the number of the day of the year and not on the number of the day of the month or the week
		evenday = IsEven(yearday)
		odday = IsOdd(yearday)
		week = [monday,tuesday,wednesday,thursday,friday,saturday,sunday]

		planned = True if ((start_time <= datehour <= end_time) or test) else False

		if planned:
			if (even == 1 and evenday) or (odd == 1 and odday):
				prog = True
			else :
				for i,day in enumerate(week):
					if day==1 and weekday==i+1:
						prog = True
	except Exception:
		logger.exception('Erreur IsProgrammed')
		prog = False
	finally:
		return prog

# update of the status of zone
# not work if bdd or nas are not visible on local network
def UpdateStatus(zone,payload,con,logger) -> None:
	try:
		AddMqttQueue(str(payload),"{0}/etat".format(zone),con,logger)
		#eng,con = DbConnect(logger)
		sql = f"update Zone set open={payload} where sv='{zone}'"
		con.execute(text(sql))
		con.commit()
		logger.debug(f"Update Zone : {zone} payload : {payload}")
	except Exception:
		logger.exception(f'Update KO : MariaDb Problem @ {config.IP_BDD_SERVER}')
	#finally:
	   #DbClose(eng,con,logger)

# "send data to mqtt brocker"
def PublishMqtt(payload,topic,logger) -> None:
	try:
		if config.PUBLISH_MQTT:
			client = mqtt.Client("arrosage_pub") #create new instance
			client.username_pw_set(username=config.USER_MQTT,password=config.PASSWORD_MQTT) #set user and password
			client.connect(host=config.IP_MQTT_BROKER,port=config.PORT_MQTT) #connect to broker
			client.publish(config.PREFIX_MQTT+"/"+config.DEVICE_MQTT+"/"+topic,str(payload),retain=True) #publish data to the specified topic
			client.disconnect() #disconnect
			logger.debug(f'Mqtt => Topic : {topic} => Payload : {payload}')
		else:
			logger.warning('Mqtt non active')
	except Exception:
		logger.exception('Probleme with Mqtt to publish data')

def AddMqttQueue(payload,topic,con,logger) -> None:
	try:
		if config.PUBLISH_MQTT:
			test = str(topic)
			topic = config.PREFIX_MQTT+"/"+config.DEVICE_MQTT+"/"+str(topic)
			payload = str(payload)
			retain = 1
			#published =0 by default
			#date_ajout = current date by default
			sql = f"insert into Mqtt_Queue (topic,payload,retain) values ('{topic}','{payload}',{retain})"
			#if test == 'parametre/coef':
			#	logger.info(sql)
			#	logger.info(topic)
			con.execute(text(sql))
			con.commit()
			logger.debug(f'Sql AddMqttQueue : {sql}')
			logger.debug(f'Mqtt => Topic : {topic} => Payload : {payload}')
		else:
			logger.warning('Mqtt non active')
	except Exception as e:
		logger.exception(f'Probleme AddMqttQueue msg {e}')

# check if the DATABASE is up
def TestDatabase(logger) -> bool:
	try:
		eng,con = DbConnect(logger)
		if eng is not None and con is not None:
			logger.debug('MariaDb OK')
			result = True
		else:
			result = False
	except Exception:
		logger.exception(f'MariaDb Not Work @ {config.IP_BDD_SERVER}')
		result = False
	finally:
		DbClose(eng, con, logger)
		return result

# check if devices on the local network are up or down
#def CheckPing(ip,logger) -> bool:
#    if os.system("ping -c 1 " + ip) == 0:
#        logger.debug(ip+ " is OK")
#        return True
#    else:
#        logger.error(ip+ " is KO")
#        return False

def CheckPing(ip,logger) -> bool:
	try:
		check_output("ping -{} 1 {}".format("n" if system().lower() == "windows" else "c", ip), shell=True)
		logger.debug(ip+ " is OK")
		result = True
	except Exception:
		logger.exception(ip+ " is KO")
		result = False
	finally:
		return result

def CheckPing_old(ip, logger) -> bool:
	try:
		socket.setdefaulttimeout(3)
		socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((ip, 80))
		logger.debug(ip+ " is OK")
		return True
	except socket.error:
		logger.exception(ip+ " is KO")
		return False

# recovery date and time of the internet or of the rtc module if the internet is not working
def GetDayTimeNtp(delta_nb_day,logger):
	try:
		client = ntplib.NTPClient()
		response = client.request('0.europe.pool.ntp.org')
		result = datetime.datetime.fromtimestamp(response.tx_time) + datetime.timedelta(days = int(delta_nb_day))
		logger.debug(f'Internet date and time as reported by NTP server: {Internet_date_and_time}')
	except Exception:
		result = datetime.datetime.today() + datetime.timedelta(days = int(delta_nb_day))
		logger.exception('Internet date and time could not be reported by server => Date from rtc module')
	finally:
		return result

# recovery date and time from local time/rtc module
def GetDayTime(delta_nb_day):
	return datetime.datetime.today() + datetime.timedelta(days = int(delta_nb_day))

# load parameters from json file
def GetJsonData(file: str,logger) -> pd.DataFrame:
	try:
		df = pd.read_json(file)
		df.reset_index(level=0, inplace=True)
		logger.debug(df)
		logger.debug(f'{file} load OK')
	except Exception:
		df = pd.DataFrame()
		logger.exception(f'Json File : {file} load KO')
	finally:
		return df

# write data to json format
def WriteJsonData(payload,file,logger) -> None:
	try:
		js = payload.to_json(orient = 'records')
		parsed = json.loads(js)
		with open(file, 'w') as outfile:
			json.dump(parsed, outfile)
		logger.debug(payload)
		logger.debug(f'{file} write OK')
	except Exception:
		logger.exception(f'File : {file} write KO')

# Log data/events for solenoid valve operation or mqtt or error
# not work if bdd or nas are not visible
def LogDatabase(val1,val2,val3,val4,val5,con,logger) -> None:
	if config.LOG_DATABASE:
		try:
			#eng,con = DbConnect(logger)
			sql = "insert into Event (val1,val2,val3,val4,val5) values ('{0}','{1}','{2}','{3}','{4}')".format(str(val1),str(val2),str(val3),str(val4),str(val5))
			con.execute(text(sql))
			con.commit()
			#con.close()
			logger.debug(f"Val1 : {val1}, Val2 : {val2}, Val3 : {val3}, Val4 : {val4}, Val5 : {val5}")
		except Exception:
			logger.exception(f'Log KO : MariaDb Problem @ {config.IP_BDD_SERVER}')
		#finally:
			#DbClose(eng,con,logger)
	else:
		logger.warning('LogDatabase désactivé')

# display the active zones on the lcd screen
# works with the column status on the database
# data comes from the last time the json file was updated if the database is down
def DisplayActiveZone(lcd,lcdsleep,con,logger) -> None:
	try:
		z = 'Aucune'
		s = 'Aucune'
		sequences = []
		zones = []
		az = LoadData("select sz.sv,sz.EndDate,z.open,sz.sequence from SequenceZone as sz inner join Zone as z on z.sv=sz.sv where z.open=1",logger,con)
		if not az.empty:
			az = az[['sv','open','EndDate','sequence']]
			sequences = az['sequence'].unique().tolist()

			for i,sequence in enumerate(sequences):
				if i==0:
					s = sequence
				else:
					s = s + ',' + sequence
			logger.debug(f'Sequence active : {s}')
			lcd.lcd_display_string("Sequence Active :   ",3)
			for i in range(1,21-len(s)) :
				s=s+' '
			lcd.lcd_display_string("{0}".format(s),4)
			time.sleep(lcdsleep)
			zones = az['sv'].unique().tolist()
			for i,zone in enumerate(zones):
				if i==0:
					z = zone
				else:
					z = z + ',' + zone
			logger.debug(f'zone active : {z}')
			lcd.lcd_display_string("Zone Active :       ",3)
			for i in range(1,21-len(z)) :
				z=z+' '
			lcd.lcd_display_string(z,4)
			time.sleep(lcdsleep)
			for index, row in az.iterrows():
				z = "Zone : {0}".format(row['sv'])
				for i in range(1,21-len(z)) :
					z=z+' '
				lcd.lcd_display_string("{0}".format(z),3)
				EndHour = '=> Fin : {0}H{1}'.format('0'+str(row["EndDate"].hour) if  row["EndDate"].hour<10 else row["EndDate"].hour,'0'+str(row["EndDate"].minute) if  row["EndDate"].minute<10 else row["EndDate"].minute)
				for i in range(1,21-len(EndHour)) :
					EndHour=EndHour+' '
				lcd.lcd_display_string(EndHour,4)
				time.sleep(lcdsleep)
		else:
			lcd.lcd_display_string("Sequence Active :   ",1)
			lcd.lcd_display_string("Aucune              ",2)
			time.sleep(lcdsleep)
			lcd.lcd_display_string("Zone Active :       ",1)
			lcd.lcd_display_string("Aucune              ",2)
			time.sleep(lcdsleep)
			logger.debug("no active sequence")
			logger.debug("no active zone")
	except Exception:
		logger.exception("Erreur DisplayActiveZone")

def MqttStatusZoneSequence(con,logger) -> None:
	try:
		z = 'Aucune'
		s = 'Aucune'
		sequences = []
		zones = []
		az = LoadData("select z.sv,z.sequence from Zone as z where z.open=1",logger,con)
		if not az.empty:
			az = az[['sv','sequence']]
			sequences = az['sequence'].unique().tolist()
			for i,sequence in enumerate(sequences):
				if i==0:
					s = sequence
				else:
					s = s + ' - ' + sequence
			zones = az['sv'].unique().tolist()
			for i,zone in enumerate(zones):
				if i==0:
					z = zone
				else:
					z = z + ' - ' + zone
		logger.debug(f'Zone active : {z}')
		logger.debug(f'Sequence active : {s}')
		AddMqttQueue(s,"status/sequence_active",con,logger)
		AddMqttQueue(z,"status/zone_active",con,logger)
		AddMqttQueue(len(sequences),"status/nb_sequence_active",con,logger)
		AddMqttQueue(len(zones),"status/nb_zone_active",con,logger)
		if len(z)>0:
			AddMqttQueue("1","status/arrosage",con,logger)
		else:
			AddMqttQueue("0","status/arrosage",con,logger)
	except Exception:
		logger.exception('Erreur MqttStatusZoneSequence')

def DisplaySequence(lcd,lcdsleep,con,logger) -> None:
	try:
		sequence = LoadData("select sz.*,z.open as svopen from SequenceZone as sz inner join Zone as z on z.sv=sz.sv order by sz.sequence,sz.order,sz.sv",logger,con)
		if not sequence.empty:
			for index,row in sequence.iterrows():
				lcd.lcd_clear()
				lcd.lcd_display_string(f'Sequence : {row["sequence"]}',1)
				lcd.lcd_display_string(f'# {row["order"]} Zone : {row["sv"]}',2)
				lcd.lcd_display_string('Debut => : {0}H{1}'.format('0'+str(row["StartingDate"].hour) if  row["StartingDate"].hour<10 else row["StartingDate"].hour,'0'+str(row["StartingDate"].minute) if  row["StartingDate"].minute<10 else row["StartingDate"].minute),3)
				lcd.lcd_display_string('=> Fin : {0}H{1}'.format('0'+str(row["EndDate"].hour) if  row["EndDate"].hour<10 else row["EndDate"].hour,'0'+str(row["EndDate"].minute) if  row["EndDate"].minute<10 else row["EndDate"].minute),4)
				time.sleep(lcdsleep)
			lcd.lcd_clear()
		else:
			logger.warning("Pas de sequence en bdd")
	except Exception as e:
		logger.exception(f"Erreur DisplaySequence msg : {e}")

def MqttProgZone(con,logger) -> None:
	try:
		zone = LoadData("SELECT b.sv,(case when a.sv is null then '-' else concat(DATE_FORMAT(a.StartingDate, '%d-%m %H:%i'),' => ',DATE_FORMAT(a.EndDate, '%H:%i')) end) as seq, (case when a.sv is null then 0 else a.planned end) as planned FROM Zone as b left join SequenceZone as a on a.sv=b.sv order by a.`order`,a.sv",logger,con)
		if not zone.empty:
			zone = zone[['sv','seq','planned']]
			for index, row in zone.iterrows():
				AddMqttQueue(row["seq"],f"{row['sv']}/sheduling",con,logger)
				AddMqttQueue(row["planned"],f"{row['sv']}/planned",con,logger)
	except Exception as e:
		logger.exception(f'Erreur MqttProgZone msg : {e}')

def UpdateSequence(table,df,con,engine,logger) -> None:
	try:
		dfseq = df.copy()
		if not dfseq.empty:
			dfseq['StartingDateMs'] = pd.to_datetime(dfseq['StartingDate'], unit='ms')
			dfseq['EndDateMs'] = pd.to_datetime(dfseq['EndDate'], unit='ms')
			dfseq.drop(columns=['StartingDate'],axis=1,inplace=True)
			dfseq.drop(columns=['EndDate'],axis=1,inplace=True)
			dfseq.rename(columns={"StartingDateMs": "StartingDate"},inplace=True)
			dfseq.rename(columns={"EndDateMs": "EndDate"},inplace=True)
			dfseq.sort_values(by='sv', ascending=True, inplace=True)
			dfseq['planned'] = dfseq['planned']*1
			dfseq['planned'] = dfseq['planned'].astype('int64')
			#dfseq.reset_index(level=0, inplace=True)

			#eng, con = DbConnect(logger)
			sql = f"select id_sv, sv, name, sequence,  `order`, open, duration,planned, StartingDate, EndDate from {table} order by sv"
			seqbdd = pd.read_sql(text(sql), con=con)

			if seqbdd.set_index('sv').equals(dfseq.set_index('sv')):
				logger.debug(f"Pas de modification de la sequence")
			else:
				#truncate table first
				logger.debug("Séquence modifée")
				sql = "delete from {0} where 1=1".format(table)
				#print(sql)
				con.execute(text(sql))
				con.commit()
				# insert data (sequence)
				dfseq.to_sql(table,if_exists='append',index='id_sequence',con=engine,method='multi')
				con.commit()
				logger.debug(f"{table} updated")
		else:
			logger.warning("No sequence available for update")
	except Exception:
	#else:
		logger.exception(f'MariaDb Problem @ {config.IP_BDD_SERVER} => Table : {table} not updated')
	#finally:
		#DbClose(eng,con,logger)

def UpdateSequence__OLD(table,df,con,logger) -> None:
	try:
		dfseq = df.copy()
		#eng, con = DbConnect(logger)
		#truncate table first
		sql = "truncate table {0}".format(table)
		con.execute(text(sql))
		con.commit()
		if not dfseq.empty:
			logger.debug(dfseq.head())
			dfseq['StartingDateMs'] = pd.to_datetime(dfseq['StartingDate'], unit='ms')
			dfseq['EndDateMs'] = pd.to_datetime(dfseq['EndDate'], unit='ms')
			dfseq.drop(columns=['StartingDate'],axis=1,inplace=True)
			dfseq.drop(columns=['EndDate'],axis=1,inplace=True)
			dfseq.rename(columns={"StartingDateMs": "StartingDate"},inplace=True)
			dfseq.rename(columns={"EndDateMs": "EndDate"},inplace=True)
			# insert data (sequence)
			dfseq.to_sql(table,if_exists='append',index='id_sequence',con=con,method='multi')
			logger.debug(f"{table} updated")
		else:
			logger.warning("No sequence available for update")
		#return True
	except Exception:
		logger.exception(f'MariaDb Problem @ {config.IP_BDD_SERVER} => Table : {table} not updated')
	#finally:
		#DbClose(eng,con,logger)


def UpdateData(table,field_update,payload_update,field_filter,payload_filter,case,con,logger) -> None:
	try:
		if case in ['Z','S']:
			sql = "update {0} set {1}='{2}' where {3}='{4}'".format(table,field_update,payload_update,field_filter,payload_filter)
		else:
			sql = "update {0} set {1}='{2}'".format(table,field_update,payload_update)
		logger.debug(sql)
		con.execute(text(sql))
		con.commit()
	except Exception:
		logger.exception(f'MariaDb Problem @ {config.IP_BDD_SERVER} => Table : {table} not updated for {field_update} = {payload_update} where {field_filter} = {payload_filter}')

def UpdateJson(sql: str,file: str,con,logger) -> None:
	try:
		#eng, con = DbConnect(logger)
		sv = pd.read_sql(text(sql), con=con)
		#DbClose(eng,con,logger)
		js = sv.to_json(orient = 'records')
		parsed = json.loads(js)
		#update json file
		with open(file, 'w') as outfile:
			json.dump(parsed, outfile)
		logger.debug(f'{file} updated')
		#return True
	except Exception:
		logger.exception(f'MariaDb Problem @ {config.IP_BDD_SERVER} => File : {file} not updated')
		#return False

def LoadData(sql: str,logger,con,file="") -> pd.DataFrame:
	try:
		#eng, con = DbConnect(logger)
		df = pd.read_sql(text(sql), con=con)
		logger.debug('load OK from database')
	except Exception as e:
		logger.exception(f'MariaDb Problem @ {config.IP_BDD_SERVER} msg : {e}')
		try:
			# reading the JSON data file if bdd problem
			if file!="":
				df = pd.read_json(file)
				df.reset_index(level=0, inplace=True)
				logger.debug(df)
				logger.debug(file + 'load OK')
			else:
				df = pd.DataFrame
				logger.warning('Erreur database et pas de fichier json configuré')
		except Exception:
			logger.exception('MariaDb Problem + Json => load KO')
			df = pd.DataFrame()
	finally:
		#DbClose(eng,con,logger)
		return df

def Print2Lcd(lcd,lcdsleep,clear,l1,l2,l3,l4,logger) -> None:
	try:
		if clear:
			lcd.lcd_clear()
		if len(l1)>0:
			for i in range(1,21-len(l1)) :
				l1=l1+' '
			lcd.lcd_display_string("{0}".format(l1), 1)
		if len(l2)>0:
			for i in range(1,21-len(l2)) :
				l2=l2+' '
			lcd.lcd_display_string("{0}".format(l2), 2)
		if len(l3)>0:
			for i in range(1,21-len(l3)) :
				l3=l3+' '
			lcd.lcd_display_string("{0}".format(l3), 3)
		if len(l4)>0:
			for i in range(1,21-len(l4)) :
				l4=l4+' '
			lcd.lcd_display_string("{0}".format(l4), 4)
		time.sleep(lcdsleep)
	except Exception as e:
		logger.exception(f"erreur Print2Lcd msg : {e}")

def GetPythonVersion(logger) -> str:
	try:
		#reponse = str(os.system('python3 -V'))
		result = f'Python {python_version()}'
	except Exception as e:
		result = 'none'
		logger.exception(f"erreur python version msg : {e}")
	finally:
		return result


def GetCpuTemperature(logger) -> str:
	try:
		return str(CPUTemperature()).split('=')[1].replace('>', '')
	except Exception:
		logger.error("erreur recupération cpu température")
		return '0.0'

def GetLoadAverage(logger) -> str:
	try:
		return str(LoadAverage()).split('=')[1].replace('>', '')
	except Exception:
		logger.exception("erreur recupération charge moyenne")
		return '0.0'

def GetDiskUsage(logger) -> str:
	try:
		return str(DiskUsage()).split('=')[1].replace('>', '')
	except Exception:
		logger.exception("erreur recupération utilisation sd")
		return '0.0'

def GetMemoryUsage(logger) -> float:
	try:
		return psutil.virtual_memory()[2]
	except Exception:
		logger.exception("erreur recupération charge ram (%)")
		return 0.0

def GetLocalIp(logger) -> str:
	try:
		return check_output(['hostname', '-s', '-I']).decode('utf-8')[:-1].split(' ')[0]
	except Exception:
		logger.exception("erreur recuperation ip local")
		return ''


def GetUptime(logger) -> str:
	try:
		uptime_seconds = uptime()
		days = uptime_seconds//86400
		hours = (uptime_seconds - days*86400)//3600
		minutes = (uptime_seconds - days*86400 - hours*3600)//60
		seconds = uptime_seconds - days*86400 - hours*3600 - minutes*60
		result = ("{0} jour{1} ".format(int(days), "s" if days!=1 else "") if days else "") + \
		("{0} heure{1} ".format(int(hours), "s" if hours!=1 else "") if hours else "") + \
		("{0} minute{1} ".format(int(minutes), "s" if minutes!=1 else "") if minutes else "") + \
		("{0} seconde{1} ".format(int(seconds), "s" if seconds!=1 else "") if seconds else "")
	except Exception:
		logger.exception("erreur recuperation uptime (str)")
		result = '0'
	finally:
		return result


def GetOsName(logger) -> str:
	try:
		return run("cat /etc/os-release", shell=True, check=True,universal_newlines = True,stdout = PIPE).stdout.splitlines()[3].replace("\"","").replace("VERSION=","")
	except Exception:
		logger.exception("erreur recuperation Os Name")
		return ''

def RestartRpi(logger) -> None:
	try:
		os.system("sudo reboot")
	except Exception:
		logger.exception('Erreur RestartRpi')

#simple map linear function with thresshold
def MapFunction(payload, in_min, in_max, out_min, out_max, logger) -> int:
	try:
		val = (payload - in_min) * (out_max - out_min) // (in_max - in_min) + out_min
		if val<out_min:
			result = out_min
		else:
			if val>out_max:
				result = out_max
			else:
				result = val
	except Exception:
		logger.exception('Erreur MapFunction')
		result = out_min
	finally:
		return result
#
def ComputeCoef(payload, min_temp, max_temp, min_coef, max_coef, logger) -> int:
	try:
		return int(MapFunction(payload, min_temp, max_temp, min_coef, max_coef, logger))
	except Exception:
		logger.exception('Coef not computed')
		return int(25)

#compute global coef in relation with temperature
def UpdateCoef(min_temp, max_temp, min_coef, max_coef, kpi, con, logger) -> None:
	try:
		idsensor = {
			'Max' : 20,
			'Moyenne' : 21,
			'90Percentile' : 22,
			'80Percentile' : 23,
			'70Percentile' : 24
		}
		#eng, con = DbConnect(logger)
		#coef actuel
		sql = f"select coef from Parameter limit 1"
		res = con.execute(text(sql))
		cursor = res.one_or_none()
		coef_actu = cursor[0] if cursor is not None else 25
		#mesure de ref
		sql = f"select mesure from mesure_last where id_sensor={idsensor[kpi]} limit 1"
		res = con.execute(text(sql))
		cursor = res.one_or_none()
		temp = cursor[0] if cursor is not None else 25
		#calcul
		payload = ComputeCoef(temp, min_temp, max_temp, min_coef, max_coef, logger)
		logger.debug(f'Temperature Kpi : {temp} °C')
		logger.debug(f'Coef calculé : {payload} %')
		AddMqttQueue(str(payload),"parametre/coef",con,logger)
		#logger.info(f'Coef calculé : {payload} %')
		#update si besoin
		if coef_actu != payload:
			sql = "update Parameter set coef='{0}'".format(payload)
			con.execute(text(sql))
			con.commit()
			#AddMqttQueue(payload,'parametre/coef',con,logger)
			logger.debug(f'Coef mis à jour : {payload} %')
		else:
			logger.debug(f'Coef non mis à jour : {payload} %')
	except Exception:
		logger.exception('Coef not updated erreur UpdateCoef')
	#finally:
	#    DbClose(eng,con,logger)


def LaunchTestRelais(con,logger) -> None:
	try:
		#eng, con = DbConnect(logger)
		sql = f"select mode from Parameter limit 1"
		res = con.execute(text(sql))
		cursor = res.one_or_none()
		mode = cursor[0] if cursor is not None else 'Auto'
		sql = "update Parameter set mode='Special'"
		con.execute(text(sql))
		con.commit()
		run(['python3', 'test_relais.py'])
		sql = f"update Parameter set mode={mode}"
		con.execute(text(sql))
		con.commit()
	except Exception:
		logger.exception('Erreur LaunchTestRelais')
	#finally:
		#DbClose(eng,con,logger)

def UpdateZoneOrder(con,logger) -> bool:
	try:
		result = False
		#eng, con = DbConnect(logger)
		sql ="select nb_max_sv from Parameter where verif_nb_max_sv=1 limit 1"
		setting = con.execute(text(sql))
		res_setting = setting.one_or_none()
		nb_max_sv = res_setting[0] if res_setting is not None else None
		if nb_max_sv is not None:
			sql =f"select z.sequence,z.order,max(z.sv) as sv,count(*) as nb from Zone as z inner join Sequence as s on s.seq=z.sequence where z.active=1 and s.active=1 group by z.sequence,z.order having count(*)>{int(nb_max_sv)} order by count(*) desc"
			zone = con.execute(text(sql))
			rows = zone.all()
			nbrows = len(rows)
			if nbrows>0:
				result = True
				for row in rows:
					sql = f'update Zone set `order`={int(row.order)+1} where sv="{str(row.sv)}"'
					con.execute(text(sql))
					con.commit()
					AddMqttQueue(str(int(row.order)+1),f"{str(row.sv).upper()}/ordre",con,logger)
					logger.debug(f'Ordre sequence modifié pour : {str(row.sv)} : {row.order} -> {int(row.order)+1}')
		else:
			logger.debug(f'Pas de verification du nombre de zone par ordre dans une sequence')
			result = False
	except Exception:
		logger.exception('Erreur UpdateZoneOrder')
		result = False
	finally:
		#DbClose(eng,con,logger)
		return result

def CheckZoneOrder(con,logger) -> bool:
	try:
		result = False
		#eng, con = DbConnect(logger)
		sql ="select nb_max_sv from Parameter where verif_nb_max_sv=1 limit 1"
		setting = con.execute(text(sql))
		res_setting = setting.one_or_none()
		nb_max_sv = res_setting[0] if res_setting is not None else 0
		if nb_max_sv > 0:
			sql =f"select z.sequence,z.order,count(*) as nb from Zone as z inner join Sequence as s on s.seq=z.sequence where z.active=1 and s.active=1 group by z.sequence,z.order having count(*)>{int(nb_max_sv)} order by count(*) desc"
			zone = con.execute(text(sql))
			firstrow = zone.first()
			if firstrow is not None and firstrow[2]>nb_max_sv:
				result = True
				logger.debug(f'Anomaly nb zone par ordre dans la sequence : {firstrow[0]} ordre : {firstrow[1]} nb : {firstrow[2]}')
			else:
				logger.debug('Aucune anomaly nb zone par ordre dans la sequence')
		else:
			logger.debug('Pas de test')
			result = False
	except Exception:
		logger.exception('Erreur CheckZoneOrder')
		result = False
	finally:
		#DbClose(eng,con,logger)
		return result

# Calls open weather 3.0 api for precipitation
def GetPrecipitationByDay(apikey,latitude,longitude,day,logger) -> float:
	day_rain = 0.0
	try:
		API_URL = 'https://api.openweathermap.org/data/3.0/onecall/day_summary?lat={lat}&lon={lon}&date={date}&appid={key}&units=metric&lang=fr'
		weather_history = requests.get(API_URL.format(key=apikey,
										date=day,
										lat=latitude,
										lon=longitude))
		weather_data = json.loads(weather_history.content.decode('utf-8'))
		day_rain = weather_data['precipitation']['total']
		logger.debug(f'Précipitation du jour {day} : {day_rain}')
	except Exception:
		logger.exception('Erreur GetPrecipitationByDay')
	finally:
		return day_rain

def GetTotalPrecipitation(apikey,latitude,longitude,logger,con,nb_day=3) -> float:
	total_rain = 0.0
	try:
		for i in range(0,nb_day):
			day = datetime.datetime.today() + datetime.timedelta(days=-i)
			day = day.strftime("%Y-%m-%d")
			total_rain += GetPrecipitationByDay(apikey,latitude,longitude,day,logger)
		logger.debug(f'Précipitation Total : {total_rain}')
	except Exception:
		logger.exception('Erreur GetTotalPrecipitation')
	finally:
		AddMqttQueue(str(total_rain),"status/precipitation",con,logger)
		return total_rain

def CheckTotalPrecipitation(apikey,threshold,latitude,longitude,nb_day,con,logger) -> None:

	rainfall = GetTotalPrecipitation(apikey,latitude,longitude,logger,con,nb_day)

	try:
		UpdateData("Parameter","cumul_precipitation",rainfall,"","","",con,logger)
	except Exception as e:
		logger.exception(f'Erreur maj table parametre msg : {e}')

	try:
		sql ="select mode from Parameter limit 1"
		setting = con.execute(text(sql))
		res_setting = setting.one_or_none()
		mode = res_setting[0] if res_setting is not None else ''
		if rainfall <= threshold and mode == 'Weather':
			sql ="Update Parameter set mode ='Auto'"
			con.execute(text(sql))
			con.commit()
			AddMqttQueue("Auto","parametre/mode",con,logger)
			logger.debug('Passage en mode auto => precipation < seuil')
			LogDatabase('','','Pluie','Activation','aut',con,logger)
		if rainfall > threshold and mode not in ['','Weather','Stop','Hivernage']:
			sql ="Update Parameter set mode ='Weather'"
			con.execute(text(sql))
			con.commit()
			AddMqttQueue("Weather","parametre/mode",con,logger)
			logger.warning('Passage en mode Weather => precipation > seuil')
			LogDatabase('Désactivation','Pluie',f'{rainfall} mm','','aut',con,logger)
	except Exception as e:
		logger.exception(f'Erreur CheckTotalPrecipitation msg : {e}')
	#finally:
	#    logger.debug('CheckTotalPrecipitation')


def CheckSequenceTime(con,logger) -> bool:
	try:
		result = False
		#eng, con = DbConnect(logger)
		sql ="select verif_seq_hour from Parameter where verif_seq_hour=1 limit 1"
		setting = con.execute(text(sql))
		res_setting = setting.one_or_none()
		verif_seq_hour = res_setting[0] if res_setting is not None else 0
		if verif_seq_hour > 0:
			sql =f"select DATE(min(StartingDate)) as StartingDate,DATE(max(EndDate)) as EndDate,Sequence from SequenceZone group by Sequence having DATE(min(StartingDate))<>DATE(max(EndDate))"
			seq = con.execute(text(sql))
			firstrow = seq.first()
			if firstrow is not None:
				result = True
				logger.debug(f'Anomalie Debut/fin Sequence : {firstrow[2]} Debut : {firstrow[0]} Fin : {firstrow[1]}')
			else:
				logger.debug('Aucune anomaly date debut / fin dans les sequences')
		else:
			logger.debug('Pas de test CheckSequenceTime')
			result = False
	except Exception:
		logger.exception('Erreur CheckSequenceTime')
		result = False
	finally:
		#DbClose(eng,con,logger)
		return result

def UpdateSequenceTime(con,logger) -> bool:
	try:
		#eng, con = DbConnect(logger)
		sql ="select verif_seq_hour from Parameter where verif_seq_hour=1 limit 1"
		setting = con.execute(text(sql))
		res_setting = setting.one_or_none()
		verif_seq_hour = res_setting[0] if res_setting is not None else None
		if verif_seq_hour is not None:
			sql =f"select DATE(min(StartingDate)) as StartingDate,DATE(max(EndDate)) as EndDate,Sequence,HOUR(min(StartingDate)) as StartHour,HOUR(max(EndDate)) as EndHour from SequenceZone group by Sequence having DATE(min(StartingDate))<>DATE(max(EndDate))"
			sequence = con.execute(text(sql))
			rows = sequence.all()
			nbrows = len(rows)
			if nbrows>0:
				for row in rows:
					hour = row.StartHour-1 if row.StartHour-1 >=0 else row.StartHour
					sql = f'update Sequence set heure={hour} where sequence="{str(row.Sequence)}"'
					con.execute(text(sql))
					con.commit()
					AddMqttQueue(str(hour),f"{str(row.Sequence).upper()}/heure",con,logger)
					logger.debug(f'Debut sequence modifiée sequence : {row.sequence} heure : {row.StartHour} -> {int(row.StartHour)-1}')
		else:
			logger.debug(f'Pas de verification du debut/fin de chaque sequence')
	except Exception:
		logger.exception('Erreur UpdateSequenceTime')
	#finally:
	#    DbClose(eng,con,logger)


def DbPurge(con,logger) -> None:
	try:
		sql="delete from Event where eventdate <= now() - INTERVAL '5' DAY"
		con.execute(text(sql))
		con.commit()
	except Exception as e:
		logger.exception('erreur purge table Event',e)
	try:
		sql = "delete from mesure where mesure_ts <= now() - INTERVAL '5' DAY"
		con.execute(text(sql))
		con.commit()
	except Exception as e:
		logger.excetion('erreur purge table mesure',e)
	try:
		sql = "delete from Mqtt_Queue where date_publish <= now() - INTERVAL '1' DAY and published=1"
		con.execute(text(sql))
		con.commit()
	except Exception as e:
		logger.excetion('erreur purge table mesure',e)

def SynchroMqtt(con,logger) -> None:
	# synchroniser etat des zones sur le brocker mqtt
	try:
		sql = "select sv as zone,open,active from Zone"
		result = con.execute(text(sql))
		con.commit()
		zones = result.all()
		for zone in zones:
			AddMqttQueue(str(zone.open),f"{str(zone.zone).upper()}/etat",con,logger)
			AddMqttQueue(str(zone.active),f"{str(zone.zone).upper()}/active",con,logger)
	except Exception as e:
		logger.excption('Erreur SynchroMqtt -> {e}')


def db(logger): # Décorateur paramétré
	def decorator(function): # Décorateur
		def new_function(*args, **kwargs):
			DbConnect(logger)
			ret = function(*args, **kwargs)
			DbClose(logger)
			return ret
		return new_function
	return decorator




