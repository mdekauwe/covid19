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

plot_dir = "plots"
if not os.path.exists(plot_dir):
    os.makedirs(plot_dir)

data = "data/processed"
fname = os.path.join(data, "deaths_totals.csv")
dfd = pd.read_csv(fname)

countries = sorted(dfd.country.unique().tolist())

width = 9
height = 6
fig = plt.figure(figsize=(width, height))
fig.subplots_adjust(hspace=0.05)
fig.subplots_adjust(wspace=0.05)
plt.rcParams['text.usetex'] = False
plt.rcParams['font.family'] = "sans-serif"
plt.rcParams['font.sans-serif'] = "Helvetica"
plt.rcParams['axes.labelsize'] = 14
plt.rcParams['font.size'] = 14
plt.rcParams['legend.fontsize'] = 10
plt.rcParams['xtick.labelsize'] = 14
plt.rcParams['ytick.labelsize'] = 14

ax = fig.add_subplot(111)

number_of_deaths = 10
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

    # just plot days since Nth death
    idx = np.argwhere(total > number_of_deaths)

    if len(idx) > 0 and len(total) > 0:

        total = total[idx]
        days = days[idx]
        days = [d - days[0] for d in days] # recentre at 0

        ax.plot(days, total)

ax.set_xlabel("Days since 10th death")
ax.set_ylabel("Cumulative deaths")
#plt.xscale("log")
ax.set_yscale("log")
ofname = "cumulative_deaths.pdf"
fig.savefig(os.path.join(plot_dir, ofname), bbox_inches='tight', pad_inches=0.1)
plt.show()
