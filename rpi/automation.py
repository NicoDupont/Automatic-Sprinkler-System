"""
* -----------------------------------------------------------------------------------
* Last update :   15/12/2024
* Arrosage Automatique / IrriPi
* Script for automations, diagnostics data and lcd management
* -----------------------------------------------------------------------------------
"""

#import function as func
from function import DbClose,UpdateJson,SynchroMqtt,UpdateSequenceTime,DbPurge,UpdateZoneOrder,CheckTotalPrecipitation,UpdateCoef,GetOsName,GetDiskUsage,GetLocalIp,GetPythonVersion,GetLoadAverage,ConfigLogging,Print2Lcd,DbConnect,AddMqttQueue,LoadData,GetDayTime,GetCpuTemperature,GetUptime,GetMemoryUsage,MqttStatusZoneSequence,MqttProgZone,DisplaySequence,DisplayActiveZone
from anomaly import AnomalyDetection
import lcddriver  #comment if not lcd
import yaml
import logging
import time
# parameters 
import config as config


if __name__ == '__main__':
    #--------------------------------------
    #initialise logging config
    #actual_day = GetDayTimeNtp(0,logger)
    logger = logging.getLogger(__name__)#.addHandler(logging.NullHandler())
    #logfile = "log/automation_"+str(actual_day.day)+"_"+str(actual_day.month)+"_" +str(actual_day.year)+".txt"
    logfile = "log/automation.txt"
    ConfigLogging(logger,logfile,config.LOG_LEVEL_STREAM,config.LOG_LEVEL_FILE,True)


    if config.ACTIVE_LCD:
        #initialise the lcd screen
        try:
            lcd = lcddriver.lcd()
            Print2Lcd(lcd,config.WAIT_TIME_LCD,True,"{0} {1} {2}".format(config.PROJECT_NAME,config.PROJECT_VERSION,config.PROJECT_DATE_VERSION),"Demarrage !","","",logger) 
            Print2Lcd(lcd,config.WAIT_TIME_LCD,False,"","Initialisation..."," "," ",logger) 
        except Exception as e:
            logger.exception(f"Probleme initialisation du lcd msg : {e}")
        

    cpt=0
    cpt_automation=0
    cpt_diagnostic=0
    cpt_error=0

    while True:

        cpt+=1
        cpt_automation+=1
        cpt_diagnostic+=1
        
        engine1,connection1 = DbConnect(logger)
        
        AddMqttQueue(cpt,'status/loop_automation',connection1,logger)#to know if running
        AddMqttQueue(cpt_error,'status/loop_automation_erreur',connection1,logger)#to know if error
        
        global_settings = LoadData('select * from Parameter limit 1',logger,connection1,file=config.GLOBAL_SETTINGS_FILE)
        MODE = global_settings["mode"].iloc[0]
        AUTO_COEF = global_settings["auto_coef"].iloc[0]
        KPI_AUTO_COEF = global_settings["kpi_auto_coef"].iloc[0]
        SEQUENCE_HOUR = global_settings["verif_seq_hour"].iloc[0]
        PRECIPITATION = global_settings["precipitation"].iloc[0]
        RAIN_THRESHOLD = global_settings["seuil_precipitation"].iloc[0]
        JOUR_PRECIPITATION = global_settings["nb_jour_precipitation"].iloc[0]
        CUMUL_PRECIPITATION = global_settings["cumul_precipitation"].iloc[0]
        STR_PRECIPITATION = "OUI" if global_settings["precipitation"].iloc[0] == 1 else "NON"
        actual_day = GetDayTime(0)
        str_kpi_auto_coef = KPI_AUTO_COEF if AUTO_COEF==1 else "none"
        str_auto_coef = "OUI" if AUTO_COEF==1 else "NON"
        
        
        try:
            if config.ACTIVE_LCD:
                Print2Lcd(lcd,config.WAIT_TIME_LCD,True,"","Mise a jour :","Parametres"," ",logger) 
                params_anomaly_detection = {
                        'global_settings':global_settings,
                        'IP_WEB_SERVER':config.IP_WEB_SERVER,
                        'IP_HA_SERVER':config.IP_HA_SERVER,
                        'IP_MQTT_SERVER':config.IP_MQTT_SERVER,
                        'IP_WEB':config.IP_WEB,
                        'connection':connection1,
                        'logger':logger
                    }
                anomaly = AnomalyDetection(**params_anomaly_detection)
                critique = "OUI" if anomaly[0] and anomaly[1] else "NON"
                Print2Lcd(lcd,config.WAIT_TIME_LCD,True,"Date : ","{0}-{1}-{2} {3}:{4}".format('0'+str(actual_day.day) if actual_day.day<10 else actual_day.day,'0'+str(actual_day.month) if actual_day.month<10 else actual_day.month,actual_day.year,'0'+str(actual_day.hour) if  actual_day.hour<10 else actual_day.hour,'0'+str(actual_day.minute) if  actual_day.minute<10 else actual_day.minute),"","",logger)
                if anomaly[0]:
                    Print2Lcd(lcd,config.WAIT_TIME_LCD,True,f"Nb Erreur : {str(len(anomaly[2]))}","Erreur Critique : ",critique,"",logger)
                    Print2Lcd(lcd,config.WAIT_TIME_LCD,True,"Liste Anomalie :","","","",logger)
                    for error, msg in anomaly[2].items():
                        Print2Lcd(lcd,config.WAIT_TIME_LCD,True,f"Erreur numero : {str(error)}","Message =>",msg,"",logger)
                Print2Lcd(lcd,config.WAIT_TIME_LCD,True,"Calcul Auto Coef :",str_auto_coef,"Methode :",str_kpi_auto_coef,logger)
                Print2Lcd(lcd,config.WAIT_TIME_LCD,True,"Arrosage",f"Mode : {MODE}","","",logger) 
                Print2Lcd(lcd,config.WAIT_TIME_LCD,True,f"Test Pluie : {STR_PRECIPITATION}",f'Nb Jour : {JOUR_PRECIPITATION}',f'{CUMUL_PRECIPITATION} mm / {RAIN_THRESHOLD} mm',f"Mode : {global_settings['mode'].iloc[0]}",logger)
                DisplaySequence(lcd,config.WAIT_TIME_LCD,connection1,logger)
                DisplayActiveZone(lcd,config.WAIT_TIME_LCD,connection1,logger)
                
                AddMqttQueue(cpt,'status/loop_lcd',connection1,logger)
                
        except Exception as e:
            cpt_error+=1
            logger.exception(f'Erreur automation.py partie LCD msg : {e}')
        
        try:   
            if cpt_diagnostic==3:
                cpt_diagnostic=0
                AddMqttQueue(GetCpuTemperature(logger),"status/temperature_cpu",connection1,logger)
                AddMqttQueue(GetUptime(logger),"status/uptime",connection1,logger)
                AddMqttQueue(GetMemoryUsage(logger),"status/memory_usage",connection1,logger)
                AddMqttQueue("online","status/available",connection1,logger) #for availability if use
                MqttProgZone(connection1,logger)
                AddMqttQueue(MODE,'status/mode',connection1,logger)
                AddMqttQueue(cpt,'status/loop_diagnostic',connection1,logger)#to know if error
                
        except Exception as e:
            cpt_error+=1
            logger.exception(f'Erreur automation.py partie diagnostic msg : {e}')    

        try:
            if cpt_automation==60:
                
                # maj du coef selon un kpi => calcul lineaire
                UpdateCoef(config.MIN_TEMP,config.MAX_TEMP,config.MIN_COEF,config.MAX_COEF,KPI_AUTO_COEF,connection1,logger) if AUTO_COEF == 1 else logger.debug('Auto Coef inactif')
                
                # calcul cumul precipitation
                CheckTotalPrecipitation(config.API_KEY,RAIN_THRESHOLD,config.LATITUDE,config.LONGITUDE,JOUR_PRECIPITATION,connection1,logger) if PRECIPITATION == 1 else logger.debug('Activation/desactivation de l arrosage selon les precipitations inactif')
                
                #updates the order of zones if too many zones can be active at the same time (power supply limit for sv and also the pump)
                #iterates until there are no more active zones compared to the maximum number available in operation at the same time
                # only work on individual sequence actualy
                while True:
                    res = UpdateZoneOrder(connection1,logger)
                    if res == False: 
                        break
                #change start hour of a sequence if the complete sequence from start to the end is between 2 days
                UpdateSequenceTime(connection1,logger) if SEQUENCE_HOUR == 1 else logger.debug('Modification Debut sequence inactive')
                # puge mqtt,log, sensor
                DbPurge(connection1,logger)
                # publish data to the mqtt brocker keep the database and the mqtt brocker synchronised
                SynchroMqtt(connection1,logger)
                
                #maj json files => a supprimer en 2025 ?
                UpdateJson('select sv,open,sequence from Zone where open=1',config.ACTIVE_ZONE_FILE,connection1,logger)
                UpdateJson("select a.id_sv,a.type,a.sv,a.order,a.gpio,a.name,a.open,(case when b.active=0 then 0 else a.active end) as active,a.sequence,a.duration,a.test,a.even,a.odd,a.monday,a.tuesday,a.wednesday,a.thursday,a.friday,a.saturday,a.sunday,a.coef,a.rpi from Zone as a left join Sequence as b on a.sequence=b.seq where a.type='zone'",config.ZONE_PARAMETER_FILE,connection1,logger)
                UpdateJson('select * from Parameter limit 1',config.GLOBAL_PARAMETER_FILE,connection1,logger)
                UpdateJson('select * from Sequence where active=1',config.SEQUENCE_FILE,connection1,logger)
                UpdateJson('select id_sv,sv,name,sequence,`order`,open,duration,StartingDate,EndDate from SequenceZone',config.ZONE_SEQUENCE_FILE,connection1,logger)
                UpdateJson('select * from mqtt where active=1',config.MQTT_BDD_AUTODISCOVERY_FILE,connection1,logger)
                
                
                
                AddMqttQueue(GetOsName(logger),"status/os_name",connection1,logger)
                AddMqttQueue(GetDiskUsage(logger),"status/disk_usage",connection1,logger)
                AddMqttQueue(GetLocalIp(logger),"status/local_ip",connection1,logger)
                AddMqttQueue(GetPythonVersion(logger),"status/python_version",connection1,logger)
                AddMqttQueue(GetLoadAverage(logger),"status/load_average_cpu",connection1,logger)
                
                AddMqttQueue(cpt,'status/loop_various',connection1,logger)
                cpt_automation=0
                print('fin automation')
        
        except Exception as e:
            cpt_error+=1
            logger.exception(f'Erreur automation.py partie automation msg : {e}')                                  
    
        DbClose(engine1,connection1,logger)
        logger.debug('Boucle Automation / Lcd : '+str(cpt))
        logger.debug("==============     FIN LOOP AUTOMATION / LCD       ==============")
        time.sleep(15)
        

