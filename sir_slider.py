#!/usr/bin/env python3
"""
dynamic matplotlib slider
@author: whirledsol
"""
from graph_slider import graph_slider
import numpy as np
from scipy.integrate import solve_ivp
from datetime import datetime

def start():
    duration = 90
    I_0=100
    xs = np.arange(0, duration, 1)
    Rnaught = 5.7

    def SIR(xs,params):
        """
        Predict how the number of people in each compartment can be changed through time toward the future.
        The model is formulated with the given beta and gamma.
        """
        start = datetime.now()
        print(f'loading SIR starting  {start}')
        gamma = params['gamma']
        beta = gamma * Rnaught
        S_0 = params['S_0']
        initial = [S_0,100,0]
        def SIR(t,y):
            S = y[0]
            I = y[1]
            return [-beta*S*I, beta*S*I-gamma*I, gamma*I]
        
        result =  solve_ivp(SIR, [0, duration], initial, t_eval=xs).y
        stop = datetime.now()
        elapsed = (stop-start).total_seconds()
        print(f'loading SIR complete, taking {elapsed}s')
        return result

    options = {
        'gamma':[1/30,1/5,1/30/30],
        'S_0':[2000000,3000000,500000]
    }
    graph_slider(xs,SIR,options)

if  __name__ =='__main__':start()