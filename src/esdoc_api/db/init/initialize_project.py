# -*- coding: utf-8 -*-
"""
.. module:: initialize_project.py
   :platform: Unix
   :synopsis: Initializes collection of supported projects.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db import models, session



def execute():
    """Initializes collection of supported projects.

    """
    # Global.
    i = models.Project()
    i.Name = "global"
    i.Description = "An application placeholder that acts as a null reference"
    session.insert(i)

    # Test.
    i = models.Project()
    i.Name = "Test"
    i.Description = "A test project plceholder"
    session.insert(i)

    # CMIP5.
    i = models.Project()
    i.Name = "CMIP5"
    i.Description = "Coupled Model Intercomparison Project Phase 5"
    i.URL = "http://cmip-pcmdi.llnl.gov/cmip5/"
    session.insert(i)

    # DCMIP-2012
    i = models.Project()
    i.Name = "DCMIP-2012"
    i.Description = "2012 Dynamical Core Model Intercomparison Project"
    i.URL = "http://earthsystemcog.org/projects/dcmip-2012/"
    session.insert(i)

    # QED-2013
    i = models.Project()
    i.Name = "QED-2013"
    i.Description = "2013 Statistical Downscaling Dynamical Core Model Intercomparison Project"
    i.URL = "http://earthsystemcog.org/projects/downscaling-2013/"
    session.insert(i)

    # ESPS
    i = models.Project()
    i.Name = "ESPS"
    i.Description = "Earth System Prediction Suite"
    i.URL = "https://www.earthsystemcog.org/projects/esps/"
    session.insert(i)
