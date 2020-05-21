---
title: 'iRONS: interactive Reservoir Operation Notebooks and Software for water reservoir systems simulation and optimisation'
tags:
  - Python
  - Jupyter Notebooks
  - water resource management
  - reservoir operation
authors:
  - name: Andres Peñuela
    orcid: 0000-0001-8039-975X
    affiliation: "1"
  - name: Francesca Pianosi
    orcid: 0000-0002-1516-2163
    affiliation: "1, 2"
affiliations:
 - name: Civil Engineering, University of Bristol, Bristol, BS8 1TR, UK
   index: 1
 - name: Cabot Institute, University of Bristol, BS8 1UH, UK
   index: 2
date: 15 March 2020
bibliography: paper.bib

---

# Summary
Computer-based models enable the simulation of water fluxes in water resource systems, such as reservoirs and diversions, in response to natural forcing inputs (e.g. streamflows) and human actions (e.g. abstractions/releases). As such they can be valuable tools to anticipate and compare the effects of different management decisions in the presence of potentially competing uses of water and uncertainty about future hydrological conditions [@Brown:2015]. Combined with an optimisation algorithm, simulation models can also be used to systematise the trial-and-error process and directly generate ‘optimal’ decisions, such as the optimal operating policy of a reservoir or the optimal release scheduling for the week/month ahead [@Dobson:2019].

`iRONS` is a python package that enables the simulation, forecasting and optimisation of reservoir systems. The package includes a set of interactive notebooks that demonstrate key functionalities through practical examples, and that can be run in the Jupyter environment either locally or remotely via a web browser. Hence, compared to other available packages for reservoir simulation and optimisation, such as the web-based application `ResOS` [@Jahanpour:2014] or the R package `reservoir` [@Turner:2016], `iRONS` has the advantage of combining the user-friendliness of web-based applications with the transparency and adaptability of open-source code, and provides both code and workflow examples for its use. As such, `iRONS` aims at being accessible to a range of users with more or less expertise in reservoir operation and/or computer programming, and contribute to increase the uptake of state-of-art methodologies while reducing the gap between research and practice in water resource systems analysis [@Rosenberg:2017].

# The core functions
The `iRONS` package provides a set of functions implementing typical reservoir modelling tasks, such as: estimating inflows to a reservoir, simulating operator decisions, closing the reservoir mass balance equation – in the context of both short-term forecasting and long-term predictions. The code includes a lot of comments and is generally written in a “math-like” style that aims to maximise readability, occasionally using less efficient but more legible coding options (for example, a for loop in place of vectorisation). Computational efficiency is regained by making the code compatible with the `Numba` just-in-time compiler (http://numba.pydata.org/; [@Lam:2015; @Marowka:2018]. Functions can thus be used within computationally expensive tasks (e.g. Monte Carlo simulation and multi-objective optimization). The structure of the code is modular, so to facilitate the integration of other Python functions or packages, for example the `Platypus` package for high performance multi-objective optimization (https://platypus.readthedocs.io/) or the Python version of the `SAFE` toolbox for Global Sensitivity Analysis (https://safetoolbox.info/). Modularity and legibility of the package functions also facilitates their tailoring to a variety of problems, from single to multiple reservoir systems, and their integration into other hydrological models at different scales.

# The notebooks
`Jupyter Notebooks` (http://jupyter.org/) is a literate programming environment that combines executable code, rich media, computational output and explanatory text in a single document. The result is a computational narrative that builds stronger links between code, data and results [@Perkel:2018]. The notebooks included in `iRONS` are divided in two sections:

A. Knowledge transfer. A set of simple examples to demonstrate the value of simulation and optimisation tools for water resources management – i.e. why one should use these tools in the first place. The Notebooks cover a range of concepts relevant to reservoir operation, such as: manual vs automatic calibration of rainfall-runoff models, what-if analysis vs optimisation, optimisation under conflicting objectives and under uncertainty, optimisation of release scheduling vs operating policy.

B. Implementation. A set of workflow examples showing how to apply the `iRONS` functions to more complex problems such as: generating inflow forecasts through a rainfall-runoff model (including bias correcting weather forecasts); optimising release scheduling against an inflow scenario or a forecast ensemble; optimising an operating policy against time series of historical or synthetic inflows. These Notebooks are meant to serve as a ‘learn-by-doing’ alternative to a User manual and a starting point for the user’s own application workflows [@Pianosi:2020].

To facilitate the visualization of model inputs and outputs, `iRONS` uses integrated widgets (`ipywidgets`; https://ipywidgets.readthedocs.io/) and interactive visualization libraries (`bqplot`; https://bqplot.readthedocs.io/).  `Jupyter Notebooks` can be downloaded and executed locally or they can be run on a web browser thanks to online services such as `Binder` (https://mybinder.org/) or `Microsoft Azure Notebooks` (https://notebooks.azure.com/).

# Outlook
We plan to keep updating `iRONS` with new functions and Notebooks, and are open to contributions and improvements from others. We hope `iRONS` will prove a useful tool for water practitioners and researchers, as well as teachers and students in hydrology and water resource management. More broadly, we hope `iRONS` will inspire others to develop open-source software and literate programming environments, including interactive visualisations, and use them as possible mechanisms to accelerate the uptake of new methods and tools.

# Acknowledgments 
This work is funded by the Engineering and Physical Sciences Research Council (EPSRC), grant EP/R007330/1.

# References
