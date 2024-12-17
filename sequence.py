"""
* -----------------------------------------------------------------------------------
* Last update :   16/09/2024
* Arrosage Automatique / IrriPi
* Calculate the watering sequence (start and end of each zone by sequence)(only on the current day)
* -----------------------------------------------------------------------------------
"""

import pandas as pd
import datetime



def ComputeSequence(**params) -> pd.DataFrame:
    
    def StartingDate(min1):
        starting = params['reference_date'] + datetime.timedelta(minutes = int(min1)) + datetime.timedelta(seconds = params['delay_time_sequence'])
        return starting

    def EndDate(min1,min2):
        end = params['reference_date'] + datetime.timedelta(minutes = int(min1) + int(min2))
        return end

    seq = pd.DataFrame()
    params['logger'].debug('calculate sequence for irrigation sequence number : '+str(params['sequence_number']))
    # remove non active solenoid valve from the dataframe
    sv= params['zone'][params['zone'].active.eq(1) & params['zone'].sequence.str.contains(params['sequence_number'])]

    if not sv.empty:
        params['logger'].debug("params['zone'] dans la sequence:")
        params['logger'].debug(sv.head())
        # sort by order, group by sequence order and compute real duration
        sv = sv.sort_values(by=['order'])
        sv = sv.groupby(['order'], as_index = False).agg({'duration': [max],'coef':[max]})
        sv['duration'] = ( sv['duration'] * (sv['coef']/100) * (params['global_time_coefficient']/100) ) 
        sv.columns = ["order", "duration", "coef"]
        
        #compute beginning and end for each sequence
        svlen = len(sv.index)
        sv['cumul'] = 0
        cumul = 0
        for i in range(0,svlen):
                sv.at[i,'cumul'] = cumul
                runtime = sv.at[i,'duration']
                if  runtime >= params['min_runtime'] and runtime <= params['max_runtime']:
                    cumul += runtime 
                else: 
                    if runtime < params['min_runtime']:
                        cumul += params['min_runtime'] 
                    else: 
                        cumul += params['max_runtime'] 

        sv['StartingDate'] = sv.apply(lambda row: StartingDate(row["cumul"]), axis=1)
        sv['EndDate'] = sv.apply(lambda row: EndDate(row["cumul"],row["duration"]), axis=1)
        sv['sequence'] = params['sequence_number']       
        params['logger'].debug("Head sequence calculée seq : "+str(params['sequence_number']))
        params['logger'].debug(sv.head())
        
        seq = sv[["sequence","order","StartingDate","EndDate"]]
    else:
        params['logger'].warning("Pas de zone dans cette sequence :"+str(params['sequence_number']))
        
    return seq
