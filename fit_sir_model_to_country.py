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
    time = np.arange(0, len(data), 1)

    sol = solve_ivp(lambda t, y: SIR(t, y, beta, gamma), t_span=[0, size],
                    y0=[S0, I0, R0], t_eval=time, vectorized=True)

    return np.sqrt(np.mean((sol.y[1] - data)**2))

def fit_model(dates, confirmed, S0, I0, R0):

    p_guess = [0.001, 0.001] # beta, gamma
    optimal = minimize(rmse, p_guess, args=(confirmed, S0, I0, R0), \
                       method='L-BFGS-B', bounds=[(0.00000001, 0.4),
                       (0.00000001, 0.4)])

    beta_fit, gamma_fit = optimal.x

    return (beta_fit, gamma_fit)


if __name__ == "__main__":

    data = "data/processed"
    fname = os.path.join(data, "confirmed_totals.csv")
    df = pd.read_csv(fname)

    S0 = 10000 # set something sensible
    I0 = 1     # set something sensible
    R0 = 2     # set something sensible
    country = "China"

    df = df[df['country'].str.match(country)]
    df.reset_index(drop=True, inplace=True)
    df = df.drop("country", axis=1).T
    df.columns = [''] * len(df.columns)

    dates = df.index.values
    confirmed = df.values.flatten()

    (beta, gamma) = fit_model(dates, confirmed, S0, I0, R0)

    print(beta, gamma)
