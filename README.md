# COVID SIM
Various Python3 Tools to Analyze Daily COVID data.

## Setup
```bash
pip install -r requirements.txt
./covid_sim.py
```

## The Data
These modules assume the data is cloned from the (CSSEGISandData repo)[https://github.com/CSSEGISandData/COVID-19] into the parent directory.

## covid_sim.py: An assortment of visualizations

This script runs various **crunches** (quick calculations or visualizations) synchronously depending on which data is deemed *interesting* by the developer.

The coding style for this project is meant to be **hasty, yet flexible** due to the changing nature of the pandemic and the data formatting of the source.

## sir_learner.py: Rudimentary SIR Modeler
Base code originally developed by (Lewuathe)[https://github.com/Lewuathe/COVID19-SIR]. This version includes various modifications. 

### Modifications
- To improve performance time, units are normalized by the US population size
- bounds have been altered to confirm to the estimated R_0 value
- testing bias in confirmed cases accounted for by adding a constant: ```confirmed_mult``` parameter
- "Recovered" in this model takes into account both Deaths+Recovered from the datasets

