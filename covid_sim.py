#!/usr/bin/env python3
"""
covid_sim.py
driver
@author: whirledsol
"""
import os
from covid_sim_crunches import *



def start():
    PATH_BASE = os.path.expanduser('~/projects/COVID-19/csse_covid_19_data/csse_covid_19_time_series')
    OUTPUT_BASE = './out/'
    PATH_C_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_confirmed_global.csv')
    PATH_D_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_deaths_global.csv')
    PATH_R_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_recovered_global.csv')
    PATH_C_US = os.path.join(PATH_BASE,'time_series_covid19_confirmed_US.csv')
    PATH_D_US = os.path.join(PATH_BASE,'time_series_covid19_deaths_US.csv')

    crunch_deathrate_global(PATH_C_GLOBAL,PATH_D_GLOBAL)
    
    crunch_deathrate_us(PATH_C_US,PATH_D_US,important_states)

    crunch_zero_global(PATH_C_GLOBAL)
    
    crunch_delta_county(PATH_C_US, 'Bucks','Pennsylvania','Confirmed')

#    crunch_delta_us(PATH_C_US,important_states,'Confirmed')

    crunch_new_us(PATH_C_US,important_states)

    crunch_map_us(PATH_C_US)

    crunch_mapnew_us(PATH_C_US)
    




if  __name__ =='__main__':start()