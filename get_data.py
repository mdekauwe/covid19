#!/usr/bin/env python

"""
Get COVID-19 daily data from the Johns Hopkins git repo

https://github.com/CSSEGISandData

That's all folks.
"""

__author__ = "Martin De Kauwe"
__version__ = "1.0 (22.03.2020)"
__email__ = "mdekauwe@gmail.com"

import os
import csv
import sys
import urllib.request
import glob

class COVID19Data:

    def __init__(self, data_dir="data"):

        self.data_dir = data_dir
        self.base_url = ("https://github.com/CSSEGISandData/COVID-19/tree/"
                         "master/csse_covid_19_data/csse_covid_19_time_series")
        self.covid_files = {
            "confirmed_fn": "time_series_19-covid-Confirmed.csv",
            "dead_fn": "time_series_19-covid-Deaths.csv",
            "recovered_fn": "time_series_19-covid-Recovered.csv",
        }

    def clean_up_old_files(self):
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
        else:
            # remove yesterdays files
            files = glob.glob(os.path.join(self.data_dir, "*.csv"))
            for f in files:
                os.remove(f)
    
    def get_data(self):

        self.clean_up_old_files()

        for fname in self.covid_files:
            url = os.path.join(self.base_url, self.covid_files[fname])
            ofn = os.path.join(self.data_dir, self.covid_files[fname])
            urllib.request.urlretrieve(url, ofn)


if __name__ == "__main__":

    C = COVID19Data()
    C.get_data()
