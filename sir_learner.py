#!/usr/bin/env python3
"""
taken from https://www.lewuathe.com/covid-19-dynamics-with-sir-model.html
"""
import os
import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import matplotlib.pyplot as plt
from datetime import timedelta, datetime
import cProfile,pstats

COUNTRY_POPULATIONS = {"China":1433783686, "US":329064917, "Japan":126860301, "United Kingdom":67530172, "Italy":60550075, "Canada":37411047}

def start():
    PATH_BASE = os.path.expanduser('~/projects/COVID-19/csse_covid_19_data/csse_covid_19_time_series')
    PATH_TIME_CONFIRMED_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_confirmed_global.csv')
    PATH_TIME_RECOVERED_GLOBAL = os.path.join(PATH_BASE,'time_series_covid19_recovered_global.csv')

    learner = SirLearner(PATH_TIME_CONFIRMED_GLOBAL,PATH_TIME_RECOVERED_GLOBAL,'US')

    learner.train()


def loss(point, confirmed, recovered,initial):
    """
    RMSE between actual confirmed cases and the estimated infectious people with given beta and gamma.
    """
    size = len(confirmed)
    beta, gamma = point

    def SIR(t, y):
        S = y[0]
        I = y[1]
        return [-beta*S*I, beta*S*I-gamma*I, gamma*I]
    
    solution = solve_ivp(SIR, [0, size], initial, t_eval=np.arange(0, size, 1), vectorized=True)
            
    
    l1 = np.sqrt(np.mean((solution.y[1] - confirmed)**2))
    l2 = np.sqrt(np.mean((solution.y[2] - recovered)**2))

    # Put more emphasis on recovered people
    alpha = 0.1
    return alpha * l1 + (1 - alpha) * l2

class SirLearner(object):
    def __init__(self, path_confirmed,path_recovered, country):
        self.path_confirmed = path_confirmed
        self.path_recovered = path_recovered
        self.country = country
        i_0 = 5
        s_0 = 100#COUNTRY_POPULATIONS[country] - i_0
        r_0 = 0
        self.initial = [s_0,i_0,r_0]

    def load_data(self, path, country):
      """
      Load confirmed cases downloaded from HDX
      """
      df = pd.read_csv(path)
      country_df = df[df['Country/Region'] == country]
      results = country_df.iloc[0].loc['1/22/20':]
      return results

    def extend_index(self, index, new_size):
        """
        gets a datetime range until it matches the new_size
        """
        values = index.values
        current = datetime.strptime(index[-1], '%m/%d/%y')
        while len(values) < new_size:
            current = current + timedelta(days=1)
            values = np.append(values, datetime.strftime(current, '%m/%d/%y'))
        return values

    def predict(self, beta, gamma, data):
        """
        Predict how the number of people in each compartment can be changed through time toward the future.
        The model is formulated with the given beta and gamma.
        """
        predict_range = 150
        new_index = self.extend_index(data.index, predict_range)
        size = len(new_index)
        extended_actual = np.concatenate((data.values, [None] * (size - len(data.values))))

        def SIR(t,y):
            S = y[0]
            I = y[1]
            return [-beta*S*I, beta*S*I-gamma*I, gamma*I]

        return new_index, extended_actual, solve_ivp(SIR, [0, size], self.initial, t_eval=np.arange(0, size, 1))

    def train(self):
        """
        Run the optimization to estimate the beta and gamma fitting the given confirmed cases.
        """
        confirmed = self.load_data(self.path_confirmed,self.country)
        recovered = self.load_data(self.path_recovered,self.country)

        pr = cProfile.Profile()
        pr.enable()
        optimal = minimize(
            loss,
            [0.001, 0.001],
            args=(confirmed,recovered,self.initial),
            method='L-BFGS-B',
            bounds=[(0.00000001, 1), (0.00000001, 1)]
        )
        pr.disable()
        stats = pstats.Stats(pr)
        stats.sort_stats('cumtime').print_stats(0.1)
        beta, gamma = optimal.x
        print(f'Found beta={beta} and gamma={gamma} for R_0={beta/gamma}')
        
        new_index, extended_actual, prediction = self.predict(beta, gamma, confirmed)
        df = pd.DataFrame({
            'Actual': extended_actual,
            'S': prediction.y[0],
            'I': prediction.y[1],
            'R': prediction.y[2]
        }, index=new_index)
        fig, ax = plt.subplots(figsize=(15, 10))
        ax.set_title(self.country)
        df.plot(ax=ax)
        plt.show()
        fig.savefig(f"./out/{self.country}.png")



if  __name__ =='__main__':start()