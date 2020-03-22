#!/usr/bin/env python

"""
Get overall numbers

That's all folks.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (22.03.2020)"
__email__ = "mdekauwe@gmail.com"

import os
import csv
import sys
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re

data = "data/processed"
fname = os.path.join(data, "deaths_totals.csv")
dfd = pd.read_csv(fname)

fname = os.path.join(data, "confirmed_totals.csv")
dfc = pd.read_csv(fname)

fname = os.path.join(data, "recovered_totals.csv")
dfr = pd.read_csv(fname)

countries = sorted(dfd.country.unique().tolist())
pattern = r"test-[0-9]+$"

for country in countries:

    # horrible, no doubt there is an easier way...but we match two
    # countries (or more), e.g. Niger and Nigeria...hack to get past that
    df = dfd[dfd['country'].str.match(country)]
    rows, cols = df.shape
    if rows > 1:

        found = -999
        for i in range(len(df)):
            country_name_len = len(df.country.values[i])
            if country_name_len == len(country):
                found = 0
        df = df.reset_index()
        df = df[df.index == found]
        df = df.drop(['index'], axis=1)

    dates = list(df.columns[1:])
    days = np.arange(len(dates))
    total = df.values.flatten()[1:]

    idx = np.argwhere(total > 10)

    if len(idx) > 0 and len(total) > 0:

        total = total[idx]
        days = days[idx]

        days = [d - days[0] for d in days]
        

        plt.plot(days, total)
        #plt.plot(dates, total)
        xmin, xmax = plt.xlim()
        plt.xticks(np.round(np.linspace(xmin, xmax, 10), 2))
#plt.xscale("log")
plt.yscale("log")
plt.show()
