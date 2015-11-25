# -*- coding: utf-8 -*-
"""
.. module:: set_summary.py
   :platform: Unix
   :synopsis: Sets document summary index.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import sqlalchemy

import pyesdoc
from pyesdoc.ontologies import cim
from pyesdoc.utils.convert import str_to_unicode

from esdoc_api.db import cache, models, session



def parse_cim_1_misc_documentset(idx, doc):
    """Parses a cim.v1.misc.DocumentSet document.

    """
    if doc.model:
        idx.Model = unicode(doc.model.short_name)
    if doc.experiment:
        idx.Experiment = unicode(doc.experiment.short_name)


# Set of summary field parsers.
_PARSERS = {
    cim.v1.misc.DocumentSet: parse_cim_1_misc_documentset
}


def execute(ctx):
    """Creates document index.

    :param object ctx: Document processing context information.

    """
    # Initialise.
    idx = models.DocumentSummary()
    idx.Description = str_to_unicode(ctx.doc.ext.description)
    idx.Document_ID = ctx.primary.ID
    idx.Language_ID = cache.get_id(models.DocumentLanguage, pyesdoc.ESDOC_DEFAULT_LANGUAGE)

    # Set fields.
    fields = [f for f in ctx.doc.ext.summary_fields if f is not None]
    for index, field in enumerate(fields):
        field = unicode(field)
        if index == 0:
            idx.ShortName = field
        elif index == 1:
            idx.LongName = field
        else:
            setattr(idx, 'Field_0' + str(index - 1), field)

    # Invoke parser if supported.
    try:
        parser = _PARSERS[type(ctx.doc)]
    except KeyError:
        pass
    else:
        parser(idx, ctx.doc)

    # Insert.
    try:
        session.insert(idx)
    except sqlalchemy.exc.IntegrityError:
        session.rollback()

