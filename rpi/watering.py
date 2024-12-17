"""
* -----------------------------------------------------------------------------------
* Last update :   15/10/2024
* Arrosage Automatique / IrriPi
* Function managing the opening or closing of solenoid valves (via gpio)
* -----------------------------------------------------------------------------------
"""

import time
from function import IsTof,IsHst,CloseRelay,OpenRelay,IsProgrammed,UpdateStatus,LogDatabase

def Watering(**params) -> None:
    
    # global parameters for irrigation
    test_duration = params['global_settings']["duree_test"].iloc[0]
    mode = params['global_settings']["mode"].iloc[0]
    
    for index, row in params['zone_inactive'].iterrows():
        sv = row["sv"]
        gpio = row["gpio"]
        rpi_relay = row["rpi"]
        open = row["open"]
        # if solenoid valve is open :
        if params['rpi_number'] == rpi_relay:
            if IsHst(gpio) == False or open == 1:
                UpdateStatus(sv,0,params['connection'],params['logger']) 
                if not params['zone_active'].empty:
                    OpenRelay(gpio,params['logger'])
                    LogDatabase(sv,gpio,'Non Active','Désactivation','sv',params['connection'],params['logger'])
                    params['logger'].debug("Deactivation of the non-active solenoid valve : "+sv)
                                           
    # --------------------------------
    # Deactivation of all solenoid valves on 1st launch / if restart unexpectedly  or criticval anomaly detected or weather mode
    if params['iteration'] == 1 or mode in ['Stop','Hivernage','Weather'] or params['critical_anomaly'] == True:         
        for index, row in params['zone_active'].iterrows():
            gpio = row["gpio"]
            sv = row["sv"]
            rpi_relay = row["rpi"]
            sv_state = row["open"]
            if params['rpi_number'] == rpi_relay:
                if IsHst(gpio) == False or sv_state == 1:
                    OpenRelay(gpio,params['logger'])
                    UpdateStatus(sv,0,params['connection'],params['logger']) 
                    if params['iteration']==1:
                        text1 = 'First Start'
                        text2 = 'Deactivation of the solenoid valve on first start'
                    else: 
                        if params['critical_anomaly']:
                            text1 = 'Critical Anomaly'
                            text2 = 'Deactivation of the solenoid valve on Critical Anomaly'
                        else:
                            if mode in ['Stop','Hivernage','Weather']:
                                text1 = mode
                                text2 = f'Deactivation of the solenoid valve on Mode : {mode}'
                    LogDatabase(sv,gpio,text1,'Désactivation','sv',params['connection'],params['logger'])
                    params['logger'].debug(text2+sv)
    else:

        if mode == 'Test':
            params['logger'].debug("Start Test Mode")
            #Tout desactiver avant test
            for index, row in params['zone_active'].iterrows():
                gpio = row["gpio"]
                sv = row["sv"]
                rpi_relay = row["rpi"]
                sv_state = row["open"]
                if params['rpi_number'] == rpi_relay:
                    if IsHst(gpio) == False and IsTof(sv_state) == False:
                        OpenRelay(gpio,params['logger'])
                        UpdateStatus(sv,0,params['connection'],params['logger']) 
                        LogDatabase(sv,gpio,"Test",'1st Désactivation','sv',params['connection'],params['logger']) 
                        params['logger'].debug("Désactivation : {0} avant test".format(sv)) 
                        time.sleep(1)       
            for index, row in params['zone_active'].iterrows():
                gpio = row["gpio"]
                sv = row["sv"]
                rpi_relay = row["rpi"]
                sv_state = row["open"]
                if params['rpi_number'] == rpi_relay:
                    if IsHst(gpio) == True:
                        CloseRelay(gpio,params['logger'])
                        UpdateStatus(sv,1,params['connection'],params['logger'])
                        LogDatabase(sv,gpio,'Test','Activation','sv',params['connection'],params['logger']) 
                        params['logger'].debug("Test Solenoid : {0} for {1} separams['connection']ds".format(sv,test_duration))
                    time.sleep(test_duration)
                    OpenRelay(gpio,params['logger'])
                    UpdateStatus(sv,0,params['connection'],params['logger']) 
                    LogDatabase(sv,gpio,'Test','Désactivation','sv',params['connection'],params['logger'])
                    time.sleep(0.1)
            params['logger'].debug("Ending Test Mode") 
    

        if mode in ['Manuel','Domotique']:
            for index, row in params['zone_active'].iterrows():
                gpio = row["gpio"]
                sv = row["sv"]
                sv_state = row["open"]
                rpi_relay = row["rpi"]                       
                if params['rpi_number'] == rpi_relay:
                    if IsHst(gpio) == False and IsTof(sv_state) == False:
                        if not params['zone_active'].empty:
                            OpenRelay(gpio,params['logger'])
                            UpdateStatus(sv,0,params['connection'],params['logger'])
                            LogDatabase(sv,gpio,'Manuel','Désactivation','sv',params['connection'],params['logger']) 
                            params['logger'].debug("Manual deactivation Solenoid valve : "+sv)      
                            time.sleep(1)
                    # log sv already open    
                    if IsHst(gpio) == False and IsTof(sv_state) == True:
                        params['logger'].debug("Solenoid valve already opened manually : "+sv) 
                    # open sv    
                    if IsHst(gpio) == True and IsTof(sv_state) == True:
                        time.sleep(1)
                        CloseRelay(gpio,params['logger'])
                        UpdateStatus(sv,1,params['connection'],params['logger'])
                        LogDatabase(sv,gpio,'Manuel','Activation','sv',params['connection'],params['logger'])
                        params['logger'].debug("Manual activation Solenoid valve : "+sv)
                        

        if mode in ['Auto','Demande']:
            for index, row in params['zone_active'].iterrows():
                gpio = row["gpio"]
                sv_state = row["open"]
                sv = row["sv"]
                rpi_relay = row["rpi"]
                if params['rpi_number'] == rpi_relay:
                    InProgrammation = IsProgrammed(sv,row["StartingDate"],row["EndDate"],params['actual_date'],row["even"],row["odd"],row["monday"],row["tuesday"],row["wednesday"],row["thursday"],row["friday"],row["saturday"],row["sunday"],False,params['logger'])
                    # close sv
                    if IsHst(gpio) == False and InProgrammation == False:
                        if not params['zone_active'].empty or sv_state == 1:
                            OpenRelay(gpio,params['logger'])
                            UpdateStatus(sv,0,params['connection'],params['logger']) 
                            LogDatabase(sv,gpio,'Auto','Désactivation','sv',params['connection'],params['logger']) 
                            params['logger'].debug("Solenoid valve programming deactivation : "+sv)
                            time.sleep(1)
                    # sv already open 
                    if IsHst(gpio) == False and InProgrammation == True :
                        params['logger'].debug("Solenoid valve already open : "+sv)
                    # open sv
                    if IsHst(gpio) == True and InProgrammation == True :
                        time.sleep(1)
                        CloseRelay(gpio,params['logger'])
                        UpdateStatus(sv,1,params['connection'],params['logger'])
                        LogDatabase(sv,gpio,'Auto','Activation','sv',params['connection'],params['logger'])
                        params['logger'].debug("Solenoid valve programming activation : "+sv) 
