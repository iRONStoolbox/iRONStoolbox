# iRONs
The iRONs toolbox is designed to facilitate a) the communication of complex modelling and optimisation concepts, such as recursive decision-making, decision-making under uncertainty and multi-objective optimisation; b) the application of these concepts to real-world reservoir systems. Compared to other available packages such as web-based application ResOS (Jahanpour et al., 2014) and the R package reservoir (Turner and Galelli, 2016), iRONs combines both the user-friendliness of web-based applications and the transparency and adaptability of open-source packages. These are the main design principles followed in developing iRONs:

-	It must be well documented and easy to share and maintain
-	It must be accessible for a wide range of users with different computing skills
-	It must be efficient without compromising code readability
-	It must be user-friendly and offer interactive results visualization
-	It must be transparent and adaptable to different purposes

iRONs is based on the use of interactive Jupyter Notebooks (http://jupyter.org/). Jupyter Notebooks is a literate programming environment that combines executable code, rich media, computational output and explanatory text in a single document. The result is a computational narrative that builds stronger links between code, data and results (Perkel, 2018). Jupyter Notebooks can be downloaded and installed locally or they can be run on a web browser thanks to online services such as Binder (https://mybinder.org/) or Microsoft Azure Notebooks (https://notebooks.azure.com/). The iRONs source code is written in Python and uses a “math-like” style that aims to be readable by a wide range of users. In order to achieve computational efficiency and enable computationally expensive tasks (e.g. Monte Carlo simulation and multi-objective optimization), we use the Numba just-in-time compiler (http://numba.pydata.org/; Lam et al. (2015), Marowka (2018)). To facilitate the visualization of model inputs and outputs and data uncertainty, integrated widgets (ipywidgets; https://ipywidgets.readthedocs.io/) and interactive visualization libraries (bqplot; https://bqplot.readthedocs.io/) are applied. The structure of the toolbox is modular, so to facilitate the addition of new tools such as hydrological and demand models, optimizers or interactive visualization interfaces as well as to incorporate additional water resource system objectives.
iRONs is divided in two sections:

A.	Knowledge transfer: interactive Jupyter Notebooks to communicate modelling and optimisation concepts relevant for reservoir operation. This is the list of currently available Notebooks:\
&nbsp;&nbsp;&nbsp;&nbsp;1.	Jupyter Notebooks introduction:\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.a.	Simple example of how to use Jupyter Notebooks\
&nbsp;&nbsp;&nbsp;&nbsp;2.	Hydrological modelling\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.a.	Calibration and evaluation of a rainfall-runoff model\
&nbsp;&nbsp;&nbsp;&nbsp;3.	Reservoir operation\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.a.	Recursive decisions and multi-objective optimisation: optimising reservoir release scheduling under conflicting objectives\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.b.	Decision making under uncertainty: optimising reservoir release scheduling under uncertain hydrological forecasts\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.c.	Rule curves: optimising the reservoir operating policy\

B.	Implementation: computationally efficient Jupyter Notebooks to implement modelling and optimisation concepts in reservoir operation. This is the list of currently available Notebooks:\
&nbsp;&nbsp;&nbsp;&nbsp;1.	Seasonal weather forecast\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.a.	Downloading ensemble weather forecasts \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;1.b.	Bias-correction of weather forecasts \
&nbsp;&nbsp;&nbsp;&nbsp;2.	Inflow forecast\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;2.a.	Generation of reservoir inflow ensemble forecasts from weather forecasts\
&nbsp;&nbsp;&nbsp;&nbsp;3.	System operation optimization\
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.a.	Multi-objective optimisation of reservoir release scheduling \
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;3.b.	Multi-objective optimisation of reservoir operating policy

    
We anticipate to update iRONs regularly with new Notebooks and be open to contributions and improvements from other researchers and users in industry and across research communities.

Click on the button below to open iRONs on MyBinder.org so you can run, modify and interact with the Notebooks online.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONs.git/master)

## References

JAHANPOUR, M., SANDOVAL-SOLIS, S. & AFSHAR, A. 2014. A web-based application for optimization of single reservoir operation. 106, E509-E517.

LAM, S. K., PITROU, A. & SEIBERT, S. 2015. Numba: a LLVM-based Python JIT compiler. Proceedings of the Second Workshop on the LLVM Compiler Infrastructure in HPC. Austin, Texas: ACM.

MAROWKA, A. J. T. J. O. S. 2018. Python accelerators for high-performance computing. 74, 1449-1460.

PERKEL, J. M. 2018. Why Jupyter is data scientists' computational notebook of choice. Nature, 563, 145-147.

TURNER, S. W. D. & GALELLI, S. 2016. Water supply sensitivity to climate change: An R package for implementing reservoir storage analysis in global and regional impact studies. Environmental Modelling & Software, 76, 13-19.
