#!/usr/bin/env python3
"""
taken from https://www.lewuathe.com/covid-19-dynamics-with-sir-model.html
"""
import os
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize,differential_evolution
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
import cProfile,pstats
import matplotlib.dates as mdates

COUNTRY_POPULATIONS = {"China":1433783686, "US":329064917, "Japan":126860301, "United Kingdom":67530172, "Italy":60550075, "Canada":37411047}
itterations = 0
def minimize_callback(vector,convergence):
    global itterations
    itterations+=1
    #print(f"{itterations}: {vector} {convergence}")

def start():
    PATH_BASE = os.path.expanduser('~/projects/COVID-19/csse_covid_19_data/csse_covid_19_time_series')
    PATH_TIME_CONFIRMED_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_confirmed_global.csv')
    PATH_TIME_RECOVERED_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_recovered_global.csv')
    PATH_TIME_DEATHS_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_deaths_global.csv')

    learner = SirLearner(PATH_TIME_CONFIRMED_GLOBAL,PATH_TIME_RECOVERED_GLOBAL,PATH_TIME_DEATHS_GLOBAL,'US')

    learner.train()


def loss(point, confirmed, recovered, I_0):
    """
    RMSE between actual confirmed cases and the estimated infectious people with given beta and gamma.
    """
    size = len(confirmed)
    S_0, beta, gamma = point
    
    initial = [S_0,I_0,0]

    def SIR(t, y):
        S = y[0]
        I = y[1]
        R = y[2]
        return [-beta*S*I, beta*S*I-gamma*I, gamma*I]
    
    solution = solve_ivp(SIR, [0, size], initial, t_eval=np.arange(0, size, 1), vectorized=True)

    l2 = np.sqrt(np.mean((solution.y[2] - recovered)**2))      
    l1 = np.sqrt(np.mean((solution.y[1] - confirmed)**2))
    # Put more emphasis on recovered people
    alpha = 0.9
    return alpha * l1 + (1 - alpha) * l2

class SirLearner(object):
    def __init__(self, path_confirmed,path_recovered, path_deaths,country, normalization_constant=COUNTRY_POPULATIONS['US'], I_0_std = 1000, duration=360):
        self.path_confirmed = path_confirmed
        self.path_recovered = path_recovered
        self.path_deaths = path_deaths
        self.country = country

        self.normalization_constant = normalization_constant
        self.I_0 = I_0_std/normalization_constant
        self.duration = duration


    def train(self):
        """
        Run the optimization to estimate the beta and gamma fitting the given confirmed cases.
        """
        #get the data we need
        confirmed = self.load_data(self.path_confirmed,self.country)
        confirmed = confirmed[confirmed.values > self.I_0]
        recovered = self.load_data(self.path_recovered,self.country)
        recovered = recovered[-len(confirmed):]
        deaths = self.load_data(self.path_deaths,self.country)
        deaths = deaths[-len(confirmed):]

        #"recovered" in SIR model is both recovered and deaths
        recovered = recovered.add(deaths)

        #bounds
        S_0_min = max(confirmed)
        S_0_max = 0.5

        #start the minimize
        start = datetime.now()
        print(f'Starting minimize on {start}')
        optimal = differential_evolution(
            loss,
            [(S_0_min,S_0_max),(0.0000005, 1), (0.0000005, 1)],
            args=(confirmed,recovered,self.I_0),
            callback=minimize_callback
        )
        S_0, beta, gamma = optimal.x
        stop = datetime.now()
        elapsed = (stop-start).total_seconds()
        print(f'After {elapsed}s and {itterations} itterations, found S_0={S_0}, beta={beta}, gamma={gamma} for R_0={beta/gamma}')
        
        #run simulation
        prediction = self.predict(S_0, beta, gamma)

        #resize these objects
        new_index = self.extend_index(confirmed.index, self.duration)
        confirmed_extended = np.concatenate((confirmed.values, [None] * (self.duration - len(confirmed.values))))
        recovered_extended = np.concatenate((recovered.values, [None] * (self.duration - len(recovered.values))))
        
        #graph results
        df = pd.DataFrame({
            'Confirmed': confirmed_extended,
            'Recovered': recovered_extended,
            'S': prediction.y[0],
            'I': prediction.y[1],
            'R': prediction.y[2]
        }, index=new_index)

        fig, ax = plt.subplots(figsize=(15, 10))
        now = datetime.now().strftime('%Y%m%d')
        ax.set_title(f'SIR Model for {self.country} from {now}')
        
        ax.set_xticks(df.index)
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%d"))
        df.plot(ax=ax)
        plt.xticks(rotation=90)    
        
        fig.savefig(os.path.realpath(f"./out/SIR_{self.country}_{now}.png"))
        plt.show()


    def load_data(self, path, country):
      """
      Load confirmed cases downloaded from HDX
      """
      df = pd.read_csv(path)
      country_df = df[df['Country/Region'] == country]
      results = country_df.iloc[0].loc['1/22/20':]
      results = results.astype(int)
      return results.apply(lambda x: x/self.normalization_constant)

    def extend_index(self, index, new_size):
        """
        gets a datetime range until it matches the new_size
        """
        values = index.values
        current = datetime.strptime(index[-1], '%m/%d/%y')
        while len(values) < new_size:
            current = current + timedelta(days=1)
            values = np.append(values, datetime.strftime(current, '%m/%d/%y'))
        return [datetime.strptime(x,'%m/%d/%y') for x in values]

    def predict(self, S_0, beta, gamma):
        """
        Predict how the number of people in each compartment can be changed through time toward the future.
        The model is formulated with the given beta and gamma.
        """
        initial = [S_0,self.I_0,0]
        def SIR(t,y):
            S = y[0]
            I = y[1]
            return [-beta*S*I, beta*S*I-gamma*I, gamma*I]
        
        return solve_ivp(SIR, [0, self.duration], initial, t_eval=np.arange(0, self.duration, 1))



if  __name__ =='__main__':start()