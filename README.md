<left> <img src="iRONS/util/images/iRONS_logo_6.png" width = "300px"><left>
  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONS.git/master)
[![Build status](https://travis-ci.org/AndresPenuela/iRONS.svg?branch=master)](https://travis-ci.org/AndresPenuela/iRONS)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

iRONS (interactive Reservoir Operation Notebooks and Software) is a python package that enables the simulation, forecasting and optimisation of reservoir systems. The package includes a set of interactive notebooks that demonstrate key functionalities through practical examples, and that can be run in the Jupyter environment either locally or remotely via a web browser. 

**The core functions** *(you can find them in the Functions folder)*

The iRONS package provides a set of Python functions implementing typical reservoir modelling tasks, such as: estimating inflows to a reservoir, simulating operator decisions, closing the reservoir mass balance equation – in the context of both short-term forecasting and long-term predictions.

**The notebooks** *(you can find them in the Notebooks folder)*

iRONS is based on the use of interactive Jupyter Notebooks (http://jupyter.org/). Jupyter Notebooks is a literate programming environment that combines executable code, rich media, computational output and explanatory text in a single document. 
The notebooks included in iRONS are divided in two sections:

**A.	Knowledge transfer:** A set of simple examples to demonstrate the value of simulation and optimisation tools for water resources management – i.e. why one should use these tools in the first place. 

**B.	Implementation:** A set of workflow examples showing how to apply the iRONS functions to more complex problems such as: generating inflow forecasts through a rainfall-runoff model (including bias correcting weather forecasts); optimising release scheduling against an inflow scenario or a forecast ensemble; optimising an operating policy against time series of historical or synthetic inflows.

## Quick start

Click on the button below to open iRONS on MyBinder.org so you can run, modify and interact with the Notebooks online. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONS.git/master)

In the section **A - Knowledge transfer** you can start with the Notebook **iRONS/Notebooks/A - Knowledge transfer/1.a. Simple example of how to use Jupyter Notebooks.ipynb**

<img src="iRONS/util/images/Executing Simple Example.gif" width = "600px">

In the section **B - Implementation** you can start with the Notebook **iRONS/Notebooks/B - Implementation/1.b. Bias correction of weather forecasts.ipynb**

🚨 Note in the section **B - Implementation** the Notebook **iRONS/Notebooks/B - Implementation/1.a. Downloading ensemble weather forecasts.ipynb** can only be run locally after installing iRONS.

## Installing iRONS loacally

Our recommendation is that you use the Anaconda distribution to install both Python and the Jupyter Notebook locally. 

Use this link https://www.anaconda.com/download/ to install the Anaconda distribution. It includes a number of useful packages and is much easier than managing packages individually. Choose the Python 3.6 version or above depending on your operating system.

### How to download iRONS and run it locally

Open the Anaconda Prompt from the Windows menu (or a OS Terminal in Mac and Linux), and then run:
```
conda update conda
```
<right> <img src="iRONS/util/images/Executing Anaconda Prompt and Conda.gif" width = "600px"><right>
```
To download iRONS on your computer run:
```
git clone https://github.com/AndresPenuela/iRONS.git
```
Once the installation is finished, get into the folder where you have download iRONS, i.e. local iRONS folder:
```
cd iRONS
```
Now create an environment and install all dependencies (necessary libraries to run iRONS):
```
conda env create -f environment.yml --prefix irons_env
```
Then you need activate the environment:
```
conda activate ./irons_env
```
Now you need to run Jupyter Notebooks to use iRONS locally:
```
jupyter notebook
```
If you need to remove the environment beacuse you are not going to use iRONS locally anymore, first you need to deactivate the environment:
```
conda deactivate ./irons_env
```
And then remove the environment:
```
conda remove --all --prefix "./irons_env"
```
🚨 If you use JupyterLab instead of Jupyter Notebook you will need to install the following extensions:
```
jupyter labextension install @jupyter-widgets/jupyterlab-manager # install the plotly extension
jupyter labextension install bqplot@0.4.6 # install the bqplot extension
jupyter labextension install @jupyterlab/plotly-extension # install the Jupyter widgets extension
```
## Testing
To run the test functions locally you first need to install `pytest`. Open the Anaconda Prompt and then run:
```
pip install -U pytest
```
now, from the local iRONS folder, invoke `pytest` through the Python interpreter from the command line:
```
python -m pytest
```
