#!/bin/bash

rm -rf data
./get_data.py
./clean_data.py
./plot_country_trajectories.py
