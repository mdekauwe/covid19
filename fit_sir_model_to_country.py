#!/usr/bin/env python

"""
Fit SIR model to countries data. The SIR model is a very simple infectious
diesease model. It assumes once healed you have immunity.

https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology#The_SIR_model

That's all folks.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (24.03.2020)"
__email__ = "mdekauwe@gmail.com"

import os
import pandas as pd
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
import sys
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt

class SIR(object):

    def __init__(self, p_guess=[0.001, 0.001], S0=1500, I0=2, R0=2):

        self.p_guess = p_guess # beta, gamma
        self.S0 = S0
        self.I0 = I0
        self.R0 = R0

    def SIR_ode(self, t, y, params):
        """
        Function to compute derivative of the ODE system

        Susceptible: people vulnerable to exposure with infectious people
        Infectious: infected people
        Recovered: people get immunity

        where Beta controls how much of the disease is transmitted via exposure
        and gamma sets the recovery rate
        """
        # unpacking
        S, I, R = y
        beta, gamma = params

        # ODEs
        dS_dt = -beta * S * I
        dI_dt = beta * S * I - gamma * I
        dR_dt = gamma * I

        return (dS_dt, dI_dt, dR_dt)

    def rmse(self, p, data, S0, I0, R0):
        """ wrapper to fit func to obs """
        size = len(data)
        beta, gamma = p
        t = np.arange(0, len(data), 1)
        sol = solve_ivp(lambda t, y: self.SIR_ode(t, y, p), t_span=[0, size],
                        y0=[self.S0, self.I0, self.R0], t_eval=t,
                        vectorized=True)

        return np.sqrt(np.mean((sol.y[1] - data)**2))

    def fit_model(self, dates, confirmed, country):
        """ Fit the beta and gamma terms of the SIR model """
        optimal = minimize(self.rmse, self.p_guess, args=(confirmed, self.S0,
                                                          self.I0, self.R0),
                           method='L-BFGS-B', bounds=[(0.00000001, 0.4),
                           (0.00000001, 0.4)])

        beta_fit, gamma_fit = optimal.x

        return (beta_fit, gamma_fit)

    def run_simulation(self, dates, beta, gamma):

        size = len(dates)
        times = np.arange(0, len(dates), 1)
        sol = solve_ivp(lambda t, y: self.SIR_ode(t, y, [beta,gamma]),
                        t_span=[min(times),max(times)],
                        y0=[self.S0, self.I0, self.R0], t_eval=times,
                        vectorized=True)

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





if __name__ == "__main__":

    data = "data/processed"
    fname = os.path.join(data, "confirmed_totals.csv")
    df = pd.read_csv(fname)

    country = "Japan"
    df = df[df['country'].str.match(country)]
    df.reset_index(drop=True, inplace=True)
    df = df.drop("country", axis=1).T
    df.columns = [''] * len(df.columns)

    dates = df.index.values
    confirmed = df.values.flatten()

    S = SIR()
    (beta, gamma) = S.fit_model(dates, confirmed, country)
    print(beta, gamma)

    S.run_simulation(dates, beta, gamma)
