# iRONS
<left> <img src="iRONS/util/images/iRONS_logo_3.png" width = "300px"><left>
  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONS.git/master)
[![Build status](https://travis-ci.org/AndresPenuela/iRONS.svg?branch=master)](https://travis-ci.org/pySRURGS/pyGOURGS)

iRONS is a python package that enables the simulation, forecasting and optimisation of reservoir systems. The package includes a set of interactive notebooks that demonstrate key functionalities through practical examples, and that can be run in the Jupyter environment either locally or remotely via a web browser. 

**The core functions** *(you can find them in the Toolbox folder)*

The iRONS package provides a set of Python functions implementing typical reservoir modelling tasks, such as: estimating inflows to a reservoir, simulating operator decisions, closing the reservoir mass balance equation – in the context of both short-term forecasting and long-term predictions.

**The notebooks** *(you can find them in the Notebooks folder)*

iRONs is based on the use of interactive Jupyter Notebooks (http://jupyter.org/). Jupyter Notebooks is a literate programming environment that combines executable code, rich media, computational output and explanatory text in a single document. 
The notebooks included in iRONS are divided in two sections:

**A.	Knowledge transfer:** A set of simple examples to demonstrate the value of simulation and optimisation tools for water resources management – i.e. why one should use these tools in the first place. 

**B.	Implementation:** A set of workflow examples showing how to apply the iRONS functions to more complex problems such as: generating inflow forecasts through a rainfall-runoff model (including bias correcting weather forecasts); optimising release scheduling against an inflow scenario or a forecast ensemble; optimising an operating policy against time series of historical or synthetic inflows.

## Quick start

Click on the button below to open iRONs on MyBinder.org so you can run, modify and interact with the Notebooks online. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONS.git/master)

In the section **A - Knowledge transfer** you can start with the Notebook **1.a. Simple example of how to use Jupyter Notebooks.ipynb**.

In the section **B - Implementation** you can start with the Notebook **1.b. Bias correction of weather forecasts.ipynb**

🚨 Note in the section **B - Implementation** the Notebook **1.a. Downloading ensemble weather forecasts.ipynb** needs to be run locally after installing iRONS.

## Installing

To install and run iRONS locally:

```sh
pip install irons
```
🚨 Note installation option does not include the example forecast data (ECMWF forecasts netcdf files) used by the Notebooks in the section **B - Implementation**.

Or you can install directly from github.com via the repository.

```
git clone https://github.com/AndresPenuela/iRONS.git
cd iRONS
pip install -r requirements.txt --user
```
🚨 Note installation option includes the example forecast data (ECMWF forecasts netcdf files) used by the Notebooks in the section **B - Implementation**.
