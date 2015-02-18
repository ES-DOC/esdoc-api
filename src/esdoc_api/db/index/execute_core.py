"""
.. module:: esdoc_api.db.index.execute_core.py

   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL / CeCILL
   :platform: Unix, Windows
   :synopsis: Indexes core entities.

.. moduleauthor:: Earth System Documentation (ES-DOC) <dev@es-doc.org>

"""
# -*- coding: utf-8 -*-
from esdoc_api.db import (
    dao,
    models,
    session,
    utils
    )
from esdoc_api.utils import runtime as rt



class _ProcessingContextInfo(object):
    """Encapsulates processing context information."""
    def __init__(self):
        self.institutes = []


def _init(ctx):
    """Initializes processing context."""
    ctx.institutes = dao.get_all(models.Institute)
    ctx.projects = dao.get_all(models.Project)


def _index(ctx):
    """Build set of indexes."""
    def build(collection, type_of):
        """Builds index."""
        for instance in collection:
            utils.create_node(type_of, instance.Name)

    build(ctx.institutes, models.NODE_TYPE_INSTITUTE)
    build(ctx.projects, models.NODE_TYPE_PROJECT)


def execute():
    """Executes facet indexing from cmip5 project."""
    ctx = _ProcessingContextInfo()
    for func, msg in (
        (_init, "initializing context"),
        (_index, "building indexes"),
        ):
        rt.log("INDEXING :: CORE :: {0}".format(msg))
        func(ctx)
