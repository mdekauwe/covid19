#!/usr/bin/env python

"""
Clean up downloaded COVID-19 files.

Data from the Johns Hopkins git repo https://github.com/CSSEGISandData

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


def clean_data(fname, type, processed_dir):

    df = pd.read_csv(fname)
    df = df.rename(str.lower, axis='columns')
    df = df.rename({"province/state": "state", "country/region": "country",
                    "long": "lon"}, axis='columns')

    # Create a new dataframe with just todays cases
    df_today = df.drop(df.columns[4:len(df.columns)-1], axis='columns')
    df_today.columns = [*df_today.columns[:-1], type]

    ofname = os.path.join(processed_dir, "%s.csv" % (type))
    df.to_csv(ofname, index=False)

    ofname = os.path.join(processed_dir, "%s_today.csv" % (type))
    df_today.to_csv(ofname, index=False)


if __name__ == "__main__":

    data_dir = "data/raw"
    processed_dir = "data/processed"
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    files = glob.glob(os.path.join(data_dir, "*.csv"))
    for fname in files:
        type = os.path.basename(fname).split(".")[0].split("-")[-1].lower()
        clean_data(fname, type, processed_dir)
