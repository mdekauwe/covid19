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
import numpy as np

def fix_country_names(df):
    # still need to fix congo...
    for i in range(len(df)):

        if df.country[i] == "Bahamas, The":
            df.loc[i,"country"]= "Bahamas"
        elif df.country[i] == "Gambia, The":
            df.loc[i,"country"]= "Gambia"
        elif df.country[i] == "Taiwan*":
            df.loc[i,"country"]= "Taiwan"
        elif df.country[i] == "Korea, South":
            df.loc[i,"country"]= "South Korea"

    return df

def clean_data(fname, type, processed_dir):

    df = pd.read_csv(fname)
    df = df.rename(str.lower, axis='columns')
    df = df.rename({"province/state": "state", "country/region": "country",
                    "long": "lon"}, axis='columns')
    df = fix_country_names(df)

    #
    ## Create a new dataframe with just todays cases...
    #
    df_today = df.drop(df.columns[4:len(df.columns)-1], axis='columns')
    df_today.columns = [*df_today.columns[:-1], type]

    ofname = os.path.join(processed_dir, "%s.csv" % (type))
    df.to_csv(ofname, index=False)

    ofname = os.path.join(processed_dir, "%s_today.csv" % (type))
    df_today.to_csv(ofname, index=False)

    #
    ## Create dataframes with daily stuff...
    #
    data = "data/processed"
    fname = os.path.join(data, "deaths.csv")
    dfd = pd.read_csv(fname)
    dfd = fix_country_names(dfd)
    countries = sorted(dfd.country.unique().tolist())

    fname = os.path.join(data, "confirmed.csv")
    dfc = pd.read_csv(fname)
    dfc = fix_country_names(dfd)

    fname = os.path.join(data, "recovered.csv")
    dfr = pd.read_csv(fname)
    dfr = fix_country_names(dfr)


    #
    ## Clean up by country so we get totals per day, currently we have
    ## state info too
    #
    countries = sorted(dfd.country.unique().tolist())
    country = countries[0]
    df = dfd[dfd['country'].str.match(country)]
    sums = df.select_dtypes(pd.np.number).sum().rename('total')

    df = df.append(sums)
    df.loc["total","lat"] = np.nan
    df.loc["total","lon"] = np.nan
    df.loc["total","country"] = country
    df = df[df.index == "total"]
    df = df.drop(['state', 'lat', 'lon'], axis=1)

    for country in countries[1:]:
        #print(country)

        dfx = dfd[dfd['country'].str.match(country)]
        sums = dfx.select_dtypes(pd.np.number).sum().rename('total')

        dfx = dfx.append(sums)
        dfx.loc["total","lat"] = np.nan
        dfx.loc["total","lon"] = np.nan
        dfx.loc["total","country"] = country
        dfx = dfx[dfx.index == "total"]
        dfx = dfx.drop(['state', 'lat', 'lon'], axis=1)

        df = df.append(dfx)
    df = df.reset_index()
    df = df.drop(['index'], axis=1)

    ofname = os.path.join(processed_dir, "%s_totals.csv" % (type))
    df.to_csv(ofname, index=False)

if __name__ == "__main__":

    data_dir = "data/raw"
    processed_dir = "data/processed"
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)

    files = glob.glob(os.path.join(data_dir, "*.csv"))
    for fname in files:
        type = os.path.basename(fname).split(".")[0].split("-")[-1].lower()
        clean_data(fname, type, processed_dir)
        sys.exit()
