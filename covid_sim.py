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

    crunch_zero_global(PATH_C_GLOBAL,population_threshold=3000000, extreme_count=6, keep=['US'])

    crunch_probability_county(PATH_C_US, 'Bucks','Pennsylvania')

    crunch_infectper_county(PATH_C_US, 'Bucks','Pennsylvania')

    crunch_new_county(PATH_C_US, 'Bucks','Pennsylvania','Confirmed')
    
    crunch_deathrate_global(PATH_C_GLOBAL,PATH_D_GLOBAL,'US')    

    crunch_map_perpop_states(PATH_C_US)

    crunch_map_perpopnew_states(PATH_C_US)

    crunch_new_states(PATH_C_US,important_states)
    
    for state in important_states:
        crunch_map_per_county(PATH_C_US, state)
        crunch_deathrate_states(PATH_C_US,PATH_D_US,state)

    
    CT_DATA_US = queryApi('https://covidtracking.com/api/v1/us/daily.json')
    CT_DATA_STATES = queryApi('https://covidtracking.com/api/v1/states/daily.json')
    #crunch_perPositive_us(CT_DATA_STATES,'Pennsylvania')
    #crunch_perPositive_us(CT_DATA_US)
    #crunch_perOutcomes_us(CT_DATA_US)





if  __name__ =='__main__':start()