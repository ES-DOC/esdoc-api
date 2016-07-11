# -*- coding: utf-8 -*-
"""
.. module:: utils.http_validator.py
   :license: GPL/CeCIL
   :platform: Unix
   :synopsis: HTTP request validation.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import uuid
from collections import Sequence

import cerberus

from esdoc_api.utils import logger



# Invalid request HTTP response code.
_HTTP_RESPONSE_BAD_REQUEST = 400



class _RequestBodyValidator(object):
    """An HTTP request body validator.

    """
    def __init__(self, request, schema):
        """Instance initializer.

        """
        self.request = request
        self.schema = schema


    def validate(self):
        """Validates the request body.

        """
        # TODO implement using jsonschema ?
        return []


class _RequestQueryParamsValidator(cerberus.Validator):
    """An HTTP request query params validator that extends the cerberus library.

    """
    def __init__(self, schema):
        """Instance initializer.

        """
        super(_RequestQueryParamsValidator, self).__init__(schema)


    def _validate_type_uuid(self, field, value):
        """Enables validation for `uuid` schema attribute.

        """
        try:
            uuid.UUID(value)
        except ValueError:
            self._error(field, cerberus.errors.ERROR_BAD_TYPE.format('uuid'))


    def _validate_allowed_case_insensitive(self, allowed_values, field, value):
            """ {'type': 'list'} """
            value = [v.lower() for v in value]
            super(_RequestQueryParamsValidator, self)._validate_allowed(allowed_values, field, value)


def _log(handler, error):
    """Logs a security related response.

    """
    msg = "[{0}]: --> security --> {1} --> {2}"
    msg = msg.format(id(handler), handler, error)
    logger.log_web_security(msg)


def is_request_valid(handler, schema):
    """Returns a flag indicating whether an HTTP request is considered to be valid.

    """
    # Validate request.
    if isinstance(schema, str):
        validator = _RequestBodyValidator(handler.request, schema)
    else:
        validator = _RequestQueryParamsValidator(schema)
        validator.validate(handler.request.query_arguments)

    # HTTP 400 if request is invalid.
    if validator.errors:
        _log(handler, "Invalid request :: {}".format(validator.errors))
        handler.clear()
        handler.send_error(_HTTP_RESPONSE_BAD_REQUEST)

    return len(validator.errors) == 0
