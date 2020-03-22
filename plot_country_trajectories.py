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

data = "data/processed"
fname = os.path.join(data, "deaths.csv")
dfd = pd.read_csv(fname)

fname = os.path.join(data, "confirmed.csv")
dfc = pd.read_csv(fname)

fname = os.path.join(data, "recovered.csv")
dfr = pd.read_csv(fname)

countries = sorted(dfd.country.unique().tolist())


countries = ["Australia", "United Kingdom", "France", "Germany"]
for country in countries:

    df = dfd[dfd['country'].str.match(country)]
    sums = df.select_dtypes(pd.np.number).sum().rename('total')

    df = df.append(sums)
    df.loc["total","lat"] = np.nan
    df.loc["total","lon"] = np.nan
    df.loc["total","country"] = country
    df = df[df.index == "total"]
    df = df.drop(['state', 'country', 'lat', 'lon'], axis=1)

    dates = list(df.columns)
    total = df.values.flatten()

    plt.plot(dates, total)
plt.show()
