"""
* -----------------------------------------------------------------------------------
* Last update :   24/10/2024
* Arrosage Automatique / IrriPi
* Main launch script
* -----------------------------------------------------------------------------------
"""
#conda install -c conda-forge mysql-connector-python
# if numpy error on raspberrypi :
#sudo apt-get install python-dev libatlas-base-dev 
from watering import Watering
from sequence import ComputeSequence
from anomaly import AnomalyDetection,MqttStatusAnomaly
import function as func
import yaml
import time
import RPi.GPIO as GPIO
#import pandas as pd
import logging
import datetime
import pandas as pd

if __name__ == '__main__':
    #---------------------------------------
    # parameters for the script from config.yaml 
    import config as config

    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for gpio in config.list_gpio:
        GPIO.setup(gpio, GPIO.OUT)
        GPIO.output(gpio, GPIO.HIGH)

    #--------------------------------------
    #initialise logging config
    #jour = GetDayTime(0)
    logger = logging.getLogger(__name__)#.addHandler(logging.NullHandler())
    #logfile = "log/arrosage_"+str(jour.day)+"_"+str(jour.month)+"_" +str(jour.year)+".txt"
    logfile = "log/arrosage.txt"
    func.ConfigLogging(logger,logfile,config.LOG_LEVEL_STREAM,config.LOG_LEVEL_FILE,True)

    #https://stackoverflow.com/questions/5974273/python-avoid-passing-logger-reference-between-functions
    #---------------------------------------
    # NUMBER_LOOP
    i=0
    cpt_error = 0
    cpt_info = 0
    
    while True: #loop launch
        i+=1
        cpt_info+=1
        try:
            engine,connection = func.DbConnect(logger)
            func.AddMqttQueue(i,"status/loop_main",connection,logger)#to know if running
            func.AddMqttQueue(cpt_error,'status/loop_main_erreur',connection,logger)#to know if error
            try:
                actual_day = func.GetDayTime(0)
                #prev_day = GetDayTime(-1) 
                # ----------------------------------------------------
                # global settings 
                global_settings = func.LoadData('select * from Parameter limit 1',logger,connection,file=config.GLOBAL_SETTINGS_FILE)
                global_coef = global_settings["coef"].iloc[0]
                mode = global_settings["mode"].iloc[0]
                sequence_demande = global_settings["sequence_demande"].iloc[0]
                heure_demande = global_settings["heure_demande"].iloc[0]
                minute_demande = global_settings["minute_demande"].iloc[0]
                logger.debug(f'mode arrosage: {mode}')
                # ----------------------------------------------------
                # sequences settings
                sequence_settings = func.LoadData('select * from Sequence where active=1',logger,connection,file=config.SEQUENCE_FILE)
                # ----------------------------------------------------
                # zones settings
                zone_settings = func.LoadData("""select a.id_sv,a.type,a.sv,a.order,a.gpio,a.name,a.open,
                                              (case when b.active=0 then 0 else a.active end) as active,
                                              a.sequence,a.duration,a.test,a.even,a.odd,a.monday,a.tuesday,
                                              a.wednesday,a.thursday,a.friday,
                                              a.saturday,a.sunday,a.coef,a.rpi 
                                              from Zone as a 
                                              left join Sequence as b on a.sequence=b.seq 
                                              where a.type='zone'""",logger,connection,file=config.ZONE_PARAMETER_FILE)
                logger.debug("Zone:")
                logger.debug(zone_settings.head())
                # ----------------------------------------------------
                # calculate the solenoid valve launch sequence by sequence and order
                zone_active = zone_settings[zone_settings.active.eq(1)]
                logger.debug("Zone active:")
                logger.debug(zone_active.head())
                # ----------------------------------------------------
                # iterate over sequence to compute each sequence 

                ##################################################################################################
                # modifier cette partie car conflit quand plusieurs sequences actives et revoir le mode à la demande
                if not sequence_settings.empty and not zone_active.empty:
                    zone_sequence = pd.DataFrame()
                    for index, row in sequence_settings.iterrows():
                        sequence = row["seq"]
                        hstart = row["heure"]
                        mstart = row["minute"]
                        
                        if mode == 'Demande' and sequence_demande==sequence:
                            starting_date = datetime.datetime(actual_day.year, actual_day.month, actual_day.day,hour=int(heure_demande),minute=int(minute_demande))
                        else:
                            starting_date = datetime.datetime(actual_day.year, actual_day.month, actual_day.day,hour=int(hstart),minute=int(mstart))

                        params_compute_sequence = {
                            'sequence_number':sequence,
                            'reference_date':starting_date,
                            'zone':zone_active[zone_active.sequence.eq(sequence)],
                            'global_time_coefficient':global_coef,
                            'delay_time_sequence':config.DELAY_TIME_SEQUENCE,
                            'min_runtime':config.MIN_TIME_SEQUENCE,
                            'max_runtime':config.MAX_TIME_SEQUENCE,
                            'logger':logger
                        }
                        #calculation of the sequence for the watering zones by sequence number
                        zs = pd.DataFrame()
                        zs = ComputeSequence(**params_compute_sequence)
                        logger.debug("Zone Sequence:")
                        logger.debug(f"zone :{sequence}")
                        logger.debug(zone_sequence.head())
                        if not zs.empty:
                            if zone_sequence.empty:
                                zone_sequence = zs
                            else:
                                zone_sequence = pd.concat([zone_sequence,zs], ignore_index=True)
                            
                    zone_active = zone_active.merge(zone_sequence, how='left', on=['order','sequence'])
                    #filter data if no sequence active and add boolean if sv is planned today.
                    #logger.info(zone_active.head(15))
                    zone_active['planned']=zone_active.apply(lambda row: func.IsProgrammed(row["sv"],row["StartingDate"],row["EndDate"],actual_day,row["even"],row["odd"],row["monday"],row["tuesday"],row["wednesday"],row["thursday"],row["friday"],row["saturday"],row["sunday"],True,logger), axis=1)
                    zone_active= zone_active[zone_active['StartingDate'].notnull()]
                    # update calculated sequences to the database
                    #logger.info(zone_active.head())
                    func.UpdateSequence('SequenceZone',zone_active[['id_sv','sv','name','sequence','order','open','duration','StartingDate','EndDate','planned']],connection,engine,logger)

                else:
                    logger.warning('Aucune sequence ou zone active')
                    #list_columns=['id_sv', 'sv', 'order', 'gpio', 'name', 'open','active', 'sequence', 'duration', 'even', 'odd', 'monday', 'tuesday','wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'coef', 'rpi','StartingDate', 'EndDate']
                    #zone_active = pd.DataFrame(columns=list_columns)
                    #create an empty dataframe if no active zone or sequence
                    zone_active = pd.DataFrame()       #empty dataframe
                    # update calculated sequences to the database
                    func.UpdateSequence('SequenceZone',pd.DataFrame(columns=['id_sv','sv','name','sequence','order','open','duration','StartingDate','EndDate','planned']),connection,logger)

                # dataframe of gpio+sv which are not in the sequence to deactivate them if they were previously active
                zone_inactive = zone_settings[zone_settings.active.ne(1)][["gpio","sv","rpi","open"]]
                if zone_inactive.empty:
                    logger.debug("Aucune zone inactive")
                # ----------------------------------------------------
                # recover pontential anomalies 
                if config.DETECT_ANOMALY:
                    params_anomaly_detection = {
                            'global_settings':global_settings,
                            'IP_WEB_SERVER':config.IP_WEB_SERVER,
                            'IP_HA_SERVER':config.IP_HA_SERVER,
                            'IP_MQTT_SERVER':config.IP_MQTT_SERVER,
                            'IP_WEB':config.IP_WEB,
                            'connection':connection,
                            'logger':logger
                        }
                    anomaly = AnomalyDetection(**params_anomaly_detection)
                    if cpt_info==5:
                        MqttStatusAnomaly(anomaly,connection,logger)
                
                # ----------------------------------------------------
                # opening or closing control of the solenoid valves for watering
                if config.RUN_WATERING: 
                    params_watering = {
                            'iteration':i,
                            'critical_anomaly':anomaly[1],
                            'zone_inactive':zone_inactive,
                            'zone_active':zone_active,
                            'global_settings':global_settings,
                            'rpi_number':config.RPI_NUMBER,
                            'actual_date':actual_day,
                            'connection':connection,
                            'logger':logger
                        }
                    Watering(**params_watering) 
                    if cpt_info==5:
                        cpt_info=0 
                        func.MqttStatusZoneSequence(connection,logger) #push mqtt info about zone and sequence to the brocker
            except Exception as e:
            #else: 
                cpt_error+=1
                logger.exception(f'Erreur main.py msg : {e}')
        #else:
        except Exception as e:
            cpt_error+=1
            logger.exception(f'Erreur connexion bdd main.py msg : {e}')
        finally:
            try:
                func.DbClose(engine,connection,logger)
            except Exception as e:
                cpt_error+=1
                logger.exception(f'Erreur Dbclose Boucle Main msg : {e}')
            # ----------------------------------------------------
            #wait SLEEP_TIME_LOOP seconds for next loop
        time.sleep(config.SLEEP_TIME_LOOP)
        #PublishMqtt(i,"status/loop_main",logger)
        logger.debug("==============     FIN LOOP            ==============")
        logger.debug("=====================================================")
    # ----------------------------------------------------
    #after while => end of the script if we going out off the loop
    GPIO.cleanup()
    logger.error("END LOOP")
