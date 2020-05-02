#!/usr/bin/env python3
"""
dynamic matplotlib slider
@author: whirledsol
"""
from graph_slider import graph_slider
import numpy as np
from scipy.integrate import solve_ivp

def start():
    duration = 90
    I_0=100
    xs = np.arange(0, duration, 1)

    def SIR(xs,params):
        """
        Predict how the number of people in each compartment can be changed through time toward the future.
        The model is formulated with the given beta and gamma.
        """
        beta = params['beta']
        gamma = params['gamma']
        S_0 = params['S_0']
        initial = [S_0,100,0]
        def SIR(t,y):
            S = y[0]
            I = y[1]
            return [-beta*S*I, beta*S*I-gamma*I, gamma*I]
        
        return solve_ivp(SIR, [0, duration], initial, t_eval=xs).y

    options = {
        'beta':[0.00005,0.5,0.0005],
        'gamma':[0.00001,0.5,0.0005],
        'S_0':[2000000,3000000,500000]
    }
    graph_slider(xs,SIR,options)

if  __name__ =='__main__':start()