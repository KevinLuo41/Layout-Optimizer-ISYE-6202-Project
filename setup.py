#!/usr/bin/env python


import platform
import sys
from codecs import open  # To use a consistent encoding
from os import path

# Always prefer setuptools over distutils
from setuptools import find_packages, setup

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="6202-Fall2020-Proj",
    version="1.0.0",
    description="",
    long_description=long_description,
    author="Kaiwen Luo",
    author_email="kluo37@gatech.edu",
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: MacOS",
        "Programming Language :: Python :: 3",
    ],
    keywords="warehousing",
    packages=find_packages(),
    python_requires=">= 3.5", install_requires=['fbprophet']
)