# Ebola 2014 outbreak study

This repository contains various scripts to perform some analysis on data provided by WHO [here](http://apps.who.int/gho/data/node.ebola-sitrep). 
It contains surveys for countries with intense transmission (Guinea, Sierra Leone and Liberia) with some variants. 
See 'What's in here' section for more details. 

# Install

To install all used dependencies run:
```
pip install -r requirements.txt
```

OPTIONAL:
Additionally we used MongoDB to store and process some of the results hence, why if you want to use it, specify your connection string in
[db_auth.json](db_auth.json) file.

# What's in here

### Epidemic models

This module contains two implementations of epidemic models [SIR](https://institutefordiseasemodeling.github.io/Documentation/general/model-sir.html) and [SEIHR](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6326236/ 
). Model SIR comes with both vital and non vital dynamics. It is plain and simple MATH only implementation, it is NOT graph implementation of said models.
You can create their objects yourself and run calculation method or use one of the existing functions that does it for you.

### Graphs

Simple custom graph drawing using matplotlib to help analyse the problem.

### Utils

Function to insert data set to MongoDB.

### Data

Example data that we used and stored in data base, as mentioned downloaded from WHO. It shows you the structure which was later parsed into WeeklyData and drawing graph functions. Contains 
necessary, but not all, data sets used in our analysis.

### WeeklyData
Parsing class for json format from WHO.

# Running

To run simulation with epidemic models simply do:
```
python epidemic-model.py
```

To run study on ebola (which pulls data from database and creates specific objects and graphs) run:
```
python ebola-study.py
```
# Warning
I would strongly advise to create your own graph functions based instead of running those, but feel free to do tinker with those provided here.

