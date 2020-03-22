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

data_dir = "data"
