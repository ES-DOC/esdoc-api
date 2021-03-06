# -*- coding: utf-8 -*-
"""
.. module:: dcmip2012_dataset.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Encapsulates DCMIP-2012 dataset id handling.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api import db



def is_valid(dataset_id):
    """Validates a DCMIP-2012 dataset id.

    :param str dataset_id: A DCMIP-2012 dataset id.

    :returns: A flag indicating whether the id is valid or not.
    :rtype: boolean

    """
    if not dataset_id or not dataset_id.strip():
        return False
    else:
        return False if len(dataset_id.strip().split('.')) < 2 else True


def get_parsed(dataset_id):
    """Returns a parsed a DCMIP-2012 dataset id.

    :param str dataset_id: DCMIP-2012 dataset id.

    :returns: A parsed DCMIP-2012 dataset id.
    :rtype: object

    """

    class DatasetID(object):
        def __init__(self):
            self.dataset_id = dataset_id.upper()
            self.drs = self.dataset_id.split('.')
            self.project = self.drs[0]
            self.model = self.drs[1]

    return DatasetID()


def _yield_doc_by_name_criteria(parsed_id):
    """Yeilds document by name search criteria.

    """
    yield 'cim.1.software.modelcomponent', parsed_id.model


def do_search(project, parsed_id):
    """Executes document search against db.

    :param str project: Project code.
    :param object parsed_id: A parsed CMIP5 dataset identifier

    :returns: A sequence of returned documents.
    :rtype: generator

    """
    for doc_type, doc_name in _yield_doc_by_name_criteria(parsed_id):
        yield db.dao.get_document_by_name(project, doc_type, doc_name)
