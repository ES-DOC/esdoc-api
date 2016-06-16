# -*- coding: utf-8 -*-
"""
.. module:: constants.py
   :platform: Unix
   :synopsis: Constants used across web-service.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.data import get_data



# Token used to indicate that all document types are in scope.
DOCUMENT_TYPE_ALL = '*'

# Set of document types loaded from file system.
DOCUMENT_TYPES = get_data('document_types')

# Document version related constants.
DOCUMENT_VERSION_ALL = '*'
DOCUMENT_VERSION_LATEST = 'latest'
DOCUMENT_VERSIONS = [
    DOCUMENT_VERSION_ALL,
    DOCUMENT_VERSION_LATEST
    ]

# Set of institutes loaded from file system.
PROJECTS = get_data('projects')

# Set of institutes loaded from file system.
INSTITUTES = get_data('institutes')