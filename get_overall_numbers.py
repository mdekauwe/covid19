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

data = "data/processed"
fname = os.path.join(data, "deaths_today.csv")
dfd = pd.read_csv(fname)
countries = sorted(dfd.country.unique().tolist())

fname = os.path.join(data, "confirmed_today.csv")
dfc = pd.read_csv(fname)

fname = os.path.join(data, "recovered_today.csv")
dfr = pd.read_csv(fname)

print("Country", "Confirmed", "Deaths", "Recovered")
for country in countries:

    dfcx = dfc[dfc['country'].str.match(country)]
    dfdx = dfd[dfd['country'].str.match(country)]
    dfrx = dfr[dfr['country'].str.match(country)]

    print(country, np.sum(dfcx.confirmed.values),
                   np.sum(dfdx.deaths.values),
                   np.sum(dfrx.recovered.values))
