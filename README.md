# COVID SIM
Various Python3 Tools to Analyze Daily COVID data.

## Disclaimer
The recent Coronavirus Pandemic is a new part of our daily lives. It is here to stay for the foreseeable future, no matter what evolves politically or in the news cycle. Please review and follow the [CDC Guidelines](https://www.cdc.gov/coronavirus/2019-nCoV/index.html) to help protect yourself and others as we *flatten the curve* together. At minimum, please *wear a mask* during all social situations.

## Intent
This project was designed to get an raw, unbiased view of the virus's spread. It also gives a semblance of control when, as individuals, we have little impact on mitigating the virus. Python was chosen as a "quick and dirty" way to manipulate the data. I don't anticipate much feedback, but I do appreciate you taking an interest in one my side projects.

## The Data
These modules assume the data is cloned from the [CSSEGISandData repo](https://github.com/CSSEGISandData/COVID-19) into the parent directory. See Setup Instructions below.

## Instructions

### Setup
```bash
#!/bin/bash
./setup.sh
```
### Run
```bash
#!/bin/bash
./update_repo.sh
./covid_sim.py
```

## covid_sim.py: An assortment of visualizations

This script runs various **crunches** (quick calculations or visualizations) synchronously depending on recent trends and geographical variances in the pandemic.

The coding style for this project is meant to be **hasty, yet flexible** due to the constantly changing nature of the source's data formatting.

## sir_learner.py: Rudimentary SIR Modeler
Base code originally developed by [Lewuathe](https://github.com/Lewuathe/COVID19-SIR). This version includes various modifications. 

### Modifications
- To improve performance time, units are normalized by the US population size
- bounds have been altered to confirm to the estimated R_0 value
- testing bias in confirmed cases accounted for by adding a constant: ```confirmed_mult``` parameter
- "Recovered" in this model takes into account both Deaths+Recovered from the datasets

