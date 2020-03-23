#!/usr/bin/env python

"""
Fit SIR model to countries data

That's all folks.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (23.03.2020)"
__email__ = "mdekauwe@gmail.com"

from sir_model import SIR
import os
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import sys
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

def rmse(p, data, S0, I0, R0):

    size = len(data)
    beta, gamma = p
    t = np.arange(0, len(data), 1)
    sol = solve_ivp(lambda t, y: SIR(t, y, p), t_span=[0, size],
                    y0=[S0, I0, R0], t_eval=t, vectorized=True)

    return np.sqrt(np.mean((sol.y[1] - data)**2))

def fit_model(dates, confirmed, S0, I0, R0):

    p_guess = [0.001, 0.001] # beta, gamma
    optimal = minimize(rmse, p_guess, args=(confirmed, S0, I0, R0), \
                       method='L-BFGS-B', bounds=[(0.00000001, 0.4),
                       (0.00000001, 0.4)])

    beta_fit, gamma_fit = optimal.x

    return (beta_fit, gamma_fit)


def test():

    # plot timeseries, made up numbers to check integrator
    beta = 0.1
    gamma = 0.05
    S0 = 10
    I0 = 0.01
    R0 = 2
    size = 100
    times = np.arange(0, size, 1)
    sol = solve_ivp(lambda t, y: SIR(t, y, [beta,gamma]),
                    t_span=[min(times),max(times)],
                    y0=[S0, I0, R0], t_eval=times, vectorized=True)

    ss = sol.y[0]
    ii = sol.y[1]
    rr = sol.y[2]
    times = sol.t

    plt.plot(times, ss, label="Susceptible")
    plt.plot(times, ii, label="Infectious")
    plt.plot(times, rr, label="Recovered")
    plt.legend(numpoints=1)
    plt.show()


if __name__ == "__main__":

    #test()
    #sys.exit()

    data = "data/processed"
    fname = os.path.join(data, "confirmed_totals.csv")
    df = pd.read_csv(fname)

    S0 = 1500      # set something sensible
    I0 = 2          # set something sensible
    R0 = 2         # set something sensible
    country = "Japan"

    df = df[df['country'].str.match(country)]
    df.reset_index(drop=True, inplace=True)
    df = df.drop("country", axis=1).T
    df.columns = [''] * len(df.columns)

    dates = df.index.values
    confirmed = df.values.flatten()

    (beta, gamma) = fit_model(dates, confirmed, S0, I0, R0)
    print(beta, gamma)

    size = len(dates)
    times = np.arange(0, len(dates), 1)
    sol = solve_ivp(lambda t, y: SIR(t, y, [beta,gamma]),
                    t_span=[min(times),max(times)],
                    y0=[S0, I0, R0], t_eval=times, vectorized=True)

    ss = sol.y[0]
    ii = sol.y[1]
    rr = sol.y[2]
    times = sol.t

    plt.plot(times, confirmed, label="observed")
    plt.plot(times, ss, label="Susceptible")
    plt.plot(times, ii, label="Infectious")
    plt.plot(times, rr, label="Recovered")
    plt.legend(numpoints=1)
    plt.show()
