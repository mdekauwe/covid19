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


def generate_future_dates(dates, confirmed, prediction_range):

    current = dt.datetime.strptime(dates[-1], '%m/%d/%y')
    while len(dates) < prediction_range:
        current = current + dt.timedelta(days=1)
        dates = np.append(dates, dt.datetime.strftime(current, '%m/%d/%y'))

    size = len(dates)
    new_confirmed = np.concatenate((confirmed, [None] * \
                                    (size - len(confirmed))))

    return (dates, new_confirmed)


if __name__ == "__main__":

    data = "data/processed"
    fname = os.path.join(data, "confirmed_totals.csv")
    df = pd.read_csv(fname)

    country = "Australia"

    df = df[df['country'].str.match(country)]
    df.reset_index(drop=True, inplace=True)
    df = df.drop("country", axis=1).T
    df.columns = [''] * len(df.columns)

    dates = df.index.values
    confirmed = df.values.flatten()
    
    (new_dates, new_confirmed) = generate_future_dates(dates, confirmed, 100)
