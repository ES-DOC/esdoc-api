# -*- coding: utf-8 -*-

"""
.. module:: handlers.publishing.create.py
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Publishing create document request handler.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
import tornado

import pyesdoc

from esdoc_api import db
from esdoc_api.utils import config
from esdoc_api.utils import exceptions
from esdoc_api.utils1.http import process_request



class DocumentCreateRequestHandler(tornado.web.RequestHandler):
    """Publishing create document request handler.

    """
    def post(self):
        """HTTP POST handler.

        """
        def _validate_request_body():
            """Parses request body.

            """
            # Decode document.
            doc = pyesdoc.decode(self.request.body, 'json')
            if not doc:
                raise exceptions.DocumentDecodingException()

            # Minimally validate document.
            if not pyesdoc.is_valid(doc):
                raise exceptions.DocumentInvalidException()

            # Validate document version.
            if doc.meta.version <= 0:
                raise exceptions.DocumentInvalidException("Version must be > 0")

            # Validate document publishing state.
            if pyesdoc.archive.exists(doc.meta.id, doc.meta.version):
                raise exceptions.DocumentPublishedException()

            # Validation passed therefore cache decoded & extended payload.
            self.doc = pyesdoc.extend(doc)


        def _ingest():
            """Ingest document.

            """
            db.session.start(config.db)
            try:
                db.ingest.execute(self.doc)
            finally:
                db.session.end()


        # Process request.
        process_request(self, [
            _validate_request_body,
            _ingest
            ])

