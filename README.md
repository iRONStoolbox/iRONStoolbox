The iRONs toolbox is designed to facilitate a) the communication of complex modelling and optimisation concepts, such as recursive decision-making, decision-making under uncertainty and multi-objective optimisation; b) the application of these concepts to real-world reservoir systems. Compared to other available packages such as web-based application ResOS (Jahanpour et al., 2014) and the R package reservoir (Turner and Galelli, 2016), iRONs combines both the user-friendliness of web-based applications and the transparency and adaptability of open-source packages. These are the main design principles followed in developing iRONs:

-	It must be well documented and easy to share and maintain
-	It must be accessible for a wide range of users with different computing skills
-	It must be efficient without compromising code readability
-	It must be user-friendly and offer interactive results visualization
-	It must be transparent and adaptable to different purposes

iRONs is based on the use of interactive Jupyter Notebooks (http://jupyter.org/). Jupyter Notebooks is a literate programming environment that combines executable code, rich media, computational output and explanatory text in a single document. The result is a computational narrative that builds stronger links between code, data and results (Perkel, 2018). Jupyter Notebooks can be downloaded and installed locally or they can be run on a web browser thanks to online services such as Binder (https://mybinder.org/) or Microsoft Azure Notebooks (https://notebooks.azure.com/). The iRONs source code is written in Python and uses a “math-like” style that aims to be readable by a wide range of users. In order to achieve computational efficiency and enable computationally expensive tasks (e.g. Monte Carlo simulation and multi-objective optimization), we use the Numba just-in-time compiler (http://numba.pydata.org/; Lam et al. (2015), Marowka (2018)). To facilitate the visualization of model inputs and outputs and data uncertainty, integrated widgets (ipywidgets; https://ipywidgets.readthedocs.io/) and interactive visualization libraries (bqplot; https://bqplot.readthedocs.io/) are applied. The structure of the toolbox is modular, so to facilitate the addition of new tools such as hydrological and demand models, optimizers or interactive visualization interfaces as well as to incorporate additional water resource system objectives.
iRONs is divided in two sections:

A -	Knowledge transfer section: interactive Jupyter Notebooks to communicate modelling and optimisation concepts relevant for reservoir operation. This section is also divided into three sections currently containing the following Notebooks:

  1 - Jupyter Notebook introduction
  
    1.a	Simple example of calibration.ipynb
    
  2 - Hydrological modelling
  
    2.a	Calibration and evaluation of a rainfall-runoff model.ipynb
    
  3 - Reservoir operation
  
    3.a	Recursive decisions and multi-objective optimisation: optimising reservoir release scheduling under conflicting objectives.ipynb
    
    3.b	Decision making under uncertainty: optimising reservoir release scheduling under uncertain hydrological forecasts.ipynb
    
    3.c	Rule curves: optimising the reservoir operating policy.ipynb

B -	Implementation: computationally efficient Jupyter Notebooks to implement modelling and optimisation concepts in reservoir operation. This section is also divided into three sections currently containing the following Notebooks:

  1 - Seasonal weather forecast
  
    1.a	Downloading ensemble weather forecasts 
    
	  1.b Bias-correction of weather forecasts 
	  
  2 - Inflow forecast
  
    2.a	Generation of reservoir inflow ensemble forecasts from weather forecasts 
    
  3 - System operation optimization
  
    3.a	Multi-objective optimisation of reservoir release scheduling 
    
    3.b	Multi-objective optimisation of reservoir operating policy
    
We anticipate to update iRONs regularly with new Notebooks and be open to contributions and improvements from other researchers and users in industry and across research communities.

# iRONs
Click on the button below to open iRONs on MyBinder.org so you can run, modify and interact with the Notebooks online.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONs.git/master)
