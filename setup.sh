#!/bin/bash

#get python ready
pip install -r requirements.txt

#extract assets
mkdir ./bin/us_counties
tar xvzf ./assets/us_counties.tar.gz -C ./bin/us_counties

#get git repo for data
git clone https://github.com/CSSEGISandData/COVID-19.git ../COVID-19