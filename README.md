<left> <img src="iRONS/util/images/iRONS_logo_6.png" width = "300px"><left>
  
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONS/HEAD?urlpath=%2Fnotebooks%2FiRONS)
[![Build status](https://travis-ci.com/AndresPenuela/iRONS.svg?branch=master)](https://travis-ci.com/AndresPenuela/iRONS)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![DOI](https://img.shields.io/badge/doi.org/10.1016/j.envsoft.2021.105188-purple.svg)](https://doi.org/10.1016/j.envsoft.2021.105188)

iRONS (interactive Reservoir Operation Notebooks and Software) is a python package that enables the simulation, forecasting and optimisation of reservoir systems. The package includes a set of interactive notebooks that demonstrate key functionalities through practical examples, and that can be run in the Jupyter environment either locally or remotely via a web browser. 

**The core functions** *(you can find them in the Software folder)*

The iRONS package provides a set of Python functions implementing typical reservoir modelling tasks, such as: estimating inflows to a reservoir, simulating operator decisions, closing the reservoir mass balance equation – in the context of both short-term forecasting and long-term predictions.

**The notebooks** *(you can find them in the Notebooks folder)*

iRONS is based on the use of interactive Jupyter Notebooks (http://jupyter.org/). Jupyter Notebooks is a literate programming environment that combines executable code, rich media, computational output and explanatory text in a single document. 
The notebooks included in iRONS are divided in two sections:

**A.	Knowledge transfer:** A set of simple examples to demonstrate the value of simulation and optimisation tools for water resources management – i.e. why one should use these tools in the first place. These two links are two examples, just click on them so you can play with them online:
[Calibration and evaluation of a rainfall runoff model](https://mybinder.org/v2/gh/AndresPenuela/iRONS/HEAD?urlpath=notebooks/iRONS/Notebooks/A%20-%20Knowledge%20transfer/2.a.%20Calibration%20and%20evaluation%20of%20a%20rainfall-runoff%20model.ipynb)

**B.	Implementation:** A set of workflow examples showing how to apply the iRONS functions to more complex problems such as: generating inflow forecasts through a rainfall-runoff model (including bias correcting weather forecasts); optimising release scheduling against an inflow scenario or a forecast ensemble; optimising an operating policy against time series of historical or synthetic inflows.
  
For a longer explanation and assessment of iRONS architecture and underpinning ideas, see: https://doi.org/10.1016/j.envsoft.2021.105188 Please cite this paper when publishing materials obtained using iRONS functions

## Quick start

Click on the button below to open iRONS on MyBinder.org so you can run, modify and interact with the Notebooks online. 

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/AndresPenuela/iRONS.git/master)

In the section **A - Knowledge transfer** you can start with the Notebook **iRONS/Notebooks/A - Knowledge transfer/1.a. Simple example of how to use Jupyter Notebooks.ipynb**. 

<img src="iRONS/util/images/Executing Simple Example.gif" width = "800px">

In the section **B - Implementation** you can start with the Notebook **iRONS/Notebooks/B - Implementation/1.a. Downloading ensemble weather forecasts.ipynb**. 

## Installing iRONS locally

Our recommendation is that you use the Anaconda distribution to install both Python and the Jupyter Notebook locally. 

Use this link https://www.anaconda.com/download/ to install the Anaconda distribution. It includes a number of useful packages and is much easier than managing packages individually. Choose the Python 3.6 version or above depending on your operating system.

Alternatively, if you already have Python you will only need to download Jupyter Notebook by running:

```
pip install notebook
```

### How to download iRONS and run it locally

Open the Anaconda Prompt from the Windows menu (or a OS Terminal in Mac and Linux), and then run:
```
conda update conda
```
<right> <img src="iRONS/util/images/Executing Anaconda Prompt and Conda.gif" width = "800px"><right>

To download iRONS you can either click on Clone button that you will find in the iRONS Github repository or you can run this on the Anaconda Prompt:
```
git clone https://github.com/AndresPenuela/iRONS.git
```
Once the download is finished, in the Anaconda Prompt get into the local iRONS folder:
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

The easiest way to test if the current version of iRONS is working is to check that the icon below shows "build passing"
[![Build status](https://travis-ci.org/AndresPenuela/iRONS.svg?branch=master)](https://travis-ci.org/AndresPenuela/iRONS)

If you have downloaded iRONS and you are using it locally you can run manually the test functions. First you need to install `pytest`. For that purpose open the Anaconda Prompt and then run:
```
pip install -U pytest
```
now, from the local iRONS folder, invoke `pytest` through the Python interpreter from the command line:
```
python -m pytest
```
