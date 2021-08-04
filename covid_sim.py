#!/usr/bin/env python3
"""
covid_sim.py
driver
@author: whirledsol
"""
import os
from covid_sim_crunches import *
from covid_sim_crunches_tracking import *



def start():
    
    PATH_BASE = '../COVID-19/csse_covid_19_data/csse_covid_19_time_series'
    OUTPUT_BASE = './out/'
    PATH_C_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_confirmed_global.csv')
    PATH_D_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_deaths_global.csv')
    PATH_R_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_recovered_global.csv')
    PATH_C_US = os.path.join(PATH_BASE,'time_series_covid19_confirmed_US.csv')
    PATH_D_US = os.path.join(PATH_BASE,'time_series_covid19_deaths_US.csv')

    important_states = ['Pennsylvania','New Jersey']


    #crunch_infectper_global(PATH_C_GLOBAL,'US')
    #crunch_infectper_county(PATH_C_US, 'Bucks','Pennsylvania')
    #crunch_infectper_county(PATH_C_US, 'Mercer','New Jersey')
    #crunch_infectper_county(PATH_C_US, 'Middlesex','New Jersey')
    #crunch_new_county(PATH_C_US, 'Bucks','Pennsylvania','Confirmed')
    #crunch_new_county(PATH_C_US, 'Mercer','New Jersey','Confirmed')
    #crunch_map_perpop_states(PATH_C_US)
    #crunch_map_perpopnew_states(PATH_C_US)
    #crunch_new_states(PATH_C_US,important_states)
    
    for state in important_states:
        #crunch_map_per_county(PATH_C_US, state)
        #crunch_deathrate_states(PATH_C_US,PATH_D_US,state)
        pass
    
    CDC_VACCINES = queryApi('https://data.cdc.gov/resource/8xkx-amqh.json')
    CDC_CASES = queryApi('https://data.cdc.gov/resource/9mfq-cb36.json')
    





if  __name__ =='__main__':start()