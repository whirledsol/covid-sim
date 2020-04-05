'''
taken from https://scipython.com/book/chapter-8-scipy/additional-examples/the-sir-epidemic-model/
'''
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt



# The SIR model differential equations.
def deriv(y, t, N, beta, gamma):
    S, I, R = y
    dSdt = -beta * S * I / N
    dIdt = beta * S * I / N - gamma * I
    dRdt = gamma * I
    return dSdt, dIdt, dRdt

def SIR(N,I0,beta,gamma,duration=120):
    '''
    Graph SIR Model
        N = Total population
        I0 = Initial number of infected
        beta =  Contact rate = R_0/mean infectious period
        gamma = mean recovery rate (in 1/days)
        duration = in days
    '''

    print(f"""SIRS MODEL
    N = {N}
    I0 = {I0}
    beta = {beta}
    gamma = {gamma}
    """)
    
    # Initial number of recovered individuals
    R0 = 0
    # Everyone else, S0, is susceptible to infection initially.
    S0 = N - I0 - R0

    # A grid of time points (in days)
    t = np.linspace(0, duration, duration)


    # Initial conditions vector
    y0 = S0, I0, R0
    # Integrate the SIR equations over the time grid, t.
    ret = odeint(deriv, y0, t, args=(N, beta, gamma))
    S, I, R = ret.T

    # Plot the data on three separate curves for S(t), I(t) and R(t)
    _, ax = plt.subplots()
    ax.plot(t, S, 'b', alpha=0.5, lw=2, label='Susceptible')
    ax.plot(t, I, 'r', alpha=0.5, lw=2, label='Infected')
    ax.plot(t, R, 'g', alpha=0.5, lw=2, label='Recovered with immunity')
    ax.set_xlabel('Time /days')
    ax.set_ylabel('Count')
    ax.set_ylim(0,1.2)
    ax.yaxis.set_tick_params(length=0)
    ax.xaxis.set_tick_params(length=0)
    ax.grid(b=True, which='major', c='w', lw=2, ls='-')
    legend = ax.legend()
    legend.get_frame().set_alpha(0.5)
    for spine in ('top', 'right', 'bottom', 'left'):
        ax.spines[spine].set_visible(False)
    plt.show()
