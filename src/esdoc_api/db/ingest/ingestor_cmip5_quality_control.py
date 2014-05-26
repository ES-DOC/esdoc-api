"""
.. module:: esdoc_api.db.ingest.ingestors.from_cmip5_questionnaire.py
   :platform: Unix, Windows
   :synopsis: CMIP5 quality control atom feed ingestor.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
from lxml import etree as et

from . base_ingestor_from_feed import FeedIngestorBase
from .. import dao
from .. models import *



# Project identifier.
_PROJECT = 'CMIP5'

# Ontology.
_ONTOLOGY = 'cim.1'



class Ingestor(FeedIngestorBase):
    """Manages ingestion from a CMIP5 QC atom feed.

    :ivar endpoint: Ingestion endpoint being processed.

    """
    def __init__(self, endpoint):
        """Constructor.

        :param endpoint: Ingestion endpoint being processed (i.e. CMIP5 quality control feed).
        :type endpoint: esdoc_api.db.models.IngestEndpoint

        """
        super(Ingestor, self).__init__(endpoint, _PROJECT, _ONTOLOGY)


    def set_institute(self, document):
        """Assign institute to qc document.

        :param document: A document being ingested.
        :type document: esdoc_api.db.models.Document

        """
        # Escape if no external id has been defined.
        if len(document.as_obj.meta.external_ids) == 0:
            return

        # Derive drs.
        drs = document.as_obj.meta.external_ids[0].value
        drs = drs.split('.')[2:]

        # Derive institute.
        if len(drs) > 0:
            institute = dao.get_by_name(Institute, drs[0].upper())
            if institute is not None:
                document.Institute_ID = institute.ID


    def ingest_feed_entry(self, content):
        """Ingests feed entry currently being processed.

        :param content: Feed entry content.
        :type content: str
        :returns: A deserialized simulation document.
        :rtype: esdoc_api.db.models.Document

        """
        # Set etree representation.
        etree = et.fromstring(content)
        nsmap = etree.nsmap
        nsmap["cim"] = nsmap.pop(None)

        # Ingest document.
        document = self.ingest_document(etree, nsmap)

        # Perform post deserialization tasks.
        self.set_institute(document)

        return document
