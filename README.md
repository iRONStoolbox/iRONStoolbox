# iRONS
![iRONS_logo](iRONS/util/images/iRONS_logo.png)

[![Travis](https://travis-ci.org/AndresPenuela/iRONS.svg?branch=master)

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONs-old.git/master)

iRONS is a python package that enables the simulation, forecasting and optimisation of reservoir systems. The package includes a set of interactive notebooks that demonstrate key functionalities through practical examples, and that can be run in the Jupyter environment either locally or remotely via a web browser. 

**The core functions** *(you can find them in the Toolbox folder)*

The iRONS package provides a set of functions implementing typical reservoir modelling tasks, such as: estimating inflows to a reservoir, simulating operator decisions, closing the reservoir mass balance equation – in the context of both short-term forecasting and long-term predictions. The code includes a lot of comments and is generally written in a “math-like” style that aims to maximise readability, occasionally using less efficient but more legible coding options (for example, a for loop in place of vectorisation). Computational efficiency is regained by making the code compatible with the Numba just-in-time compiler (http://numba.pydata.org/). The structure of the code is modular, so to facilitate the integration of other Python functions or packages, for example the Platypus package for high performance multi-objective optimization (https://platypus.readthedocs.io. Modularity and legibility of the package functions also facilitates their tailoring to a variety of problems, from single to multiple reservoir systems, and their integration into other hydrological models at different scales.

**The notebooks** *(you can find them in the Notebooks folder)*

iRONs is based on the use of interactive Jupyter Notebooks (http://jupyter.org/). Jupyter Notebooks is a literate programming environment that combines executable code, rich media, computational output and explanatory text in a single document. 
The notebooks included in iRONS are divided in two sections:


**A.	Knowledge transfer:** A set of simple examples to demonstrate the value of simulation and optimisation tools for water resources management – i.e. why one should use these tools in the first place. The Notebooks cover a range of concepts relevant to reservoir operation, such as: manual vs automatic calibration of rainfall-runoff models, what-if analysis vs optimisation, optimisation under conflicting objectives and under uncertainty, optimisation of release scheduling vs operating policy. This is the list of currently available Notebooks:\
&nbsp;&nbsp;&nbsp;&nbsp;0.	Tutorials:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.a.	Getting started with Jupyter Notebooks\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;0.b.	How to install libraries\
&nbsp;&nbsp;&nbsp;&nbsp;1.	Jupyter Notebooks introduction:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.a.	Simple example of how to use Jupyter Notebooks\
&nbsp;&nbsp;&nbsp;&nbsp;2.	Hydrological modelling:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.a.	Calibration and evaluation of a rainfall-runoff model\
&nbsp;&nbsp;&nbsp;&nbsp;3.	Reservoir operation:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.a.	Recursive decisions and multi-objective optimisation: optimising reservoir release scheduling under conflicting objectives\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.b.	Decision making under uncertainty: optimising reservoir release scheduling under uncertain hydrological forecasts\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.c.	Reservoir operating policy: optimising the release policy

**B.	Implementation:** A set of workflow examples showing how to apply the iRONS functions to more complex problems such as: generating inflow forecasts through a rainfall-runoff model (including bias correcting weather forecasts); optimising release scheduling against an inflow scenario or a forecast ensemble; optimising an operating policy against time series of historical or synthetic inflows. This is the list of currently available Notebooks:\
&nbsp;&nbsp;&nbsp;&nbsp;1.	Seasonal weather forecast:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.a.	Downloading ensemble weather forecasts \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.b.	Bias-correction of weather forecasts \
&nbsp;&nbsp;&nbsp;&nbsp;2.	Inflow forecast:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.a.	Generation of reservoir inflow ensemble forecasts from weather forecasts\
&nbsp;&nbsp;&nbsp;&nbsp;3.	System operation optimization:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.a.	Multi-objective optimisation of reservoir release scheduling \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.b.	Multi-objective optimisation of reservoir operating policy

To facilitate the visualization of model inputs and outputs and data uncertainty, integrated widgets (ipywidgets; https://ipywidgets.readthedocs.io/) and interactive visualization libraries (bqplot; https://bqplot.readthedocs.io/ and plotly;  https://plot.ly) are applied

Click on the button below to open iRONs on MyBinder.org so you can run, modify and interact with the Notebooks online.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONs-old.git/master)
