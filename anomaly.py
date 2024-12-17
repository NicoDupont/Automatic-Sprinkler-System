"""
* -----------------------------------------------------------------------------------
* Last update :   15/10/2024
* Arrosage Automatique / IrriPi
* Anomaly function
* -----------------------------------------------------------------------------------
"""
import time
import pandas as pd
from function import IsAbove,IsTof,IsBelow,TestDatabase,CheckPing,IsHst,AddMqttQueue,LogDatabase,CheckZoneOrder,CheckSequenceTime
import logging

# detect anomlies
def AnomalyDetection(**params) -> tuple:
    try:
        # global parameters for irrigation
        mode = params['global_settings']["mode"].iloc[0]
        minp = params['global_settings']["pression_seuil_bas"].iloc[0]
        maxp = params['global_settings']["pression_seuil_haut"].iloc[0]
        canalpupstream = params['global_settings']["pression_canal_amont"].iloc[0]
        canalpdownstream = params['global_settings']["pression_canal_aval"].iloc[0]
        tankpupstream = params['global_settings']["pression_cuve_amont"].iloc[0]
        tankpdownstream = params['global_settings']["pression_cuve_aval"].iloc[0]
        pville = params['global_settings']["pression_ville"].iloc[0]
        pvarrosage = params['global_settings']["pression_arrosage"].iloc[0]
        otp = params['global_settings']["test_pression_cuve"].iloc[0]
        ocp = params['global_settings']["test_pression_canal"].iloc[0]
        ovp = params['global_settings']["test_pression_ville"].iloc[0]
        minh = params['global_settings']["seuil_min_capacite_cuve"].iloc[0]
        height = params['global_settings']["hauteur_eau_cuve"].iloc[0]
        oh = params['global_settings']["test_hauteur_eau_cuve"].iloc[0]
        ws = params['global_settings']["source"].iloc[0]

        # --------------------------------
        # Condition tests for watering activation
        dict_anomaly = {}

        if (IsBelow(canalpupstream,minp) or IsAbove(canalpupstream,maxp)) and IsTof(ocp) == False and ws=="canal":
            dict_anomaly[1]="Pression Canal Am {} B".format(canalpupstream)

        if (IsBelow(canalpdownstream,minp) or IsAbove(canalpdownstream,maxp))  and IsTof(ocp) == False and ws=="canal":
            dict_anomaly[1]="Pression Canal Av {} B".format(canalpdownstream)

        if (IsBelow(tankpupstream,minp) or IsAbove(tankpupstream,maxp))  and IsTof(otp) == False and ws=="tank":
            dict_anomaly[3]="Pression Cuve Am {} B".format(tankpupstream)

        if (IsBelow(tankpdownstream,minp) or IsAbove(tankpdownstream,maxp)) and IsTof(otp) == False and ws=="tank":
            dict_anomaly[4]="Pression Cuve Av {} B".format(tankpdownstream)

        if (IsBelow(tankpupstream,minp) or IsAbove(tankpupstream,maxp))  and IsTof(ovp) == False and ws=="ville":
            dict_anomaly[5]="Pression Ville {} B".format(pville)

        if IsAbove(height,minh) == False and IsTof(oh) == False and ws=="tank":
            dict_anomaly[6]="Niveau Cuve {} L".format(height)

        if mode == 'Stop' :
            dict_anomaly[7]="Mode Stop"

        if CheckPing(params['IP_WEB'],params['logger']) == False:
            dict_anomaly[9]="Internet Offline"

        if CheckPing(params['IP_WEB_SERVER'],params['logger']) == False:
            dict_anomaly[10]="WEB Offline"

        if CheckZoneOrder(params['connection'],params['logger']) == True:
            dict_anomaly[11]="Nb Zone Active"

        if CheckSequenceTime(params['connection'],params['logger']) == True:
            dict_anomaly[12]="Ano Debut / Fin"

        if TestDatabase(params['logger']) == False:
            dict_anomaly[20]="Database Offline"

        if CheckPing(params['IP_MQTT_SERVER'],params['logger']) == False:
            dict_anomaly[21]="Brocker Mqtt Offline"
        
        if CheckPing(params['IP_HA_SERVER'],params['logger']) == False:
            dict_anomaly[22]="HomeAssistant Offline"

        # --------------------------------
        # manage potential anomalies
        anomaly = False
        critical_anomaly = False

        if len(dict_anomaly)>0:
            anomaly = True
            params['logger'].debug("liste des erreurs :")
            for error, msg in dict_anomaly.items():
                LogDatabase(error,msg,'','','ano',params['connection'],params['logger'])
                if error>=20:
                    critical_anomaly = True
                    params['logger'].error("Critical Anomaly : "+str(error)+" Message : "+str(msg))
                else:
                    params['logger'].warning("Error Number : "+str(error)+" Message : "+str(msg))     
                    
        result = [anomaly,critical_anomaly,dict_anomaly]
    except Exception:
        params['logger'].exception('Erreur Anomaly Detection')
        LogDatabase('Erreur','Anomaly Detection','','','ano',params['connection'],params['logger'])
        result = [False,False,{}]
    finally:
        return result


def MqttStatusAnomaly(anomaly: tuple,con,logger) -> None:
    try:
        if anomaly[0] or anomaly[1]:
            e = 0
            ec = 0
            for error, msg in anomaly[2].items():
                if error<20:
                    e+=1
                else:
                    ec+=1
            AddMqttQueue('{0}'.format(e),"status/nb_erreur",con,logger)
            AddMqttQueue('{0}'.format(ec),"status/nb_erreur_critique",con,logger)
            if anomaly[0]:
                AddMqttQueue('1',"status/erreur",con,logger)
            if anomaly[1]:        
                AddMqttQueue('1',"status/erreur_critique",con,logger)
        else:
            AddMqttQueue('0',"status/erreur",con,logger)
            AddMqttQueue('0',"status/erreur_critique",con,logger)
            AddMqttQueue('0',"status/nb_erreur",con,logger)
            AddMqttQueue('0',"status/nb_erreur_critique",con,logger)
    except Exception:
        logger.exception('Erreur MqttAnomaly')
        LogDatabase('Erreur','MqttAnomaly','','','ano',con,logger)