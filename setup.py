
# Always prefer setuptools over distutils
from setuptools import setup, find_packages
from os import path

from io import open

here = path.abspath(path.dirname(__file__))
# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='iRONS',  # Required
    version='0.6',  # Required
    description='A Python package that enables the simulation, forecasting and optimisation of reservoir systems',  # Optional
    long_description=long_description,  # Optional
    long_description_content_type='text/markdown',  # Optional (see note above)
    url='https://github.com/AndresPenuela/iRONS',  # Optional
    author='Andres Peñuela, Francesca Pianosi',  # Optional
    author_email='andres.penuela-fernandez@bristol.ac.uk',  # Optional
    packages=find_packages(exclude=['workflows', 'data']),  # Required
    python_requires='>=3.7',
    install_requires=[
        "numpy==1.16.5",
        "matplotlib==3.1.1",
        "ipywidgets==7.2.1",
        "bqplot==0.11.6",
		"platypus-opt==1.0.3",
		"netcdf4==1.4.2",
		"numba==0.49.1",
		"plotly==4.4.1",
		"cdsapi==0.2.5",
		"pandas==0.25.1"
    ],
)
