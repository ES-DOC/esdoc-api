# -*- coding: utf-8 -*-
"""
.. module:: utils.http.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: HTTP request handler utility functions.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import json

import tornado

from esdoc_api.utils import logger
from esdoc_api.utils.convertor import to_namedtuple
from esdoc_api.utils.http_invoker import execute as process_request
from esdoc_api.utils.http_validator import is_request_valid



# HTTP CORS header.
HTTP_HEADER_Access_Control_Allow_Origin = "Access-Control-Allow-Origin"


class HTTPRequestHandler(tornado.web.RequestHandler):
    """A web service request handler.

    """
    def decode_json_body(self, as_namedtuple=True):
        """Decodes request body JSON string.

        :param tornado.web.RequestHandler handler: A web request handler.

        :returns: Decoded json data.
        :rtype: namedtuple | None

        """
        if not self.request.body:
            return None

        body = json.loads(self.request.body)

        return to_namedtuple(body) if as_namedtuple else body


    def invoke(
        self,
        schema,
        taskset,
        error_taskset=[]
        ):
        """Invokes handler tasks.

        """
        # Log all requests.
        msg = "[{0}]: executing --> {1}"
        msg = msg.format(id(self), self)
        logger.log_web(msg)

        # Validate & process request.
        if is_request_valid(self, schema):
            process_request(self, taskset, error_taskset)
