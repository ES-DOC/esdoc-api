"""
.. module:: esdoc_api.lib.pyesdoc.serialization.py
   :copyright: @2013 Earth System Documentation (http://es-doc.org)
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Exposes document serialization functions.

.. moduleauthor:: Mark Conway-Greenslade (formerly Morgan) <momipsl@ipsl.jussieu.fr>


"""
# Module imports.
from . utils import (
    runtime as rt,
    serializer_dict,
    serializer_json,
    serializer_xml,
    serializer_xml_metafor_cim_v1
    )



# Set of supported ESDOC encodings.
ESDOC_ENCODING_DICT = 'dict'
ESDOC_ENCODING_JSON = 'json'
ESDOC_ENCODING_XML = 'xml'
METAFOR_CIM_XML_ENCODING = 'xml-metafor-cim-v1'

# Standard ESDOC encodings.
ESDOC_ENCODINGS = (
    ESDOC_ENCODING_DICT,
    ESDOC_ENCODING_JSON,
    ESDOC_ENCODING_XML
)

# Custom ESDOC encodings.
ESDOC_ENCODINGS_CUSTOM = (
    METAFOR_CIM_XML_ENCODING,
)

# Standard ESDOC encodings.
ESDOC_ENCODING_HTTP_MEDIA_TYPES = {
    ESDOC_ENCODING_JSON : "application/json",
    ESDOC_ENCODING_XML : "application/xml"
}

# Set of supported sesrializers keyed by encoding.
_serializers = {
    ESDOC_ENCODING_DICT : serializer_dict,
    ESDOC_ENCODING_JSON : serializer_json,
    ESDOC_ENCODING_XML : serializer_xml,
    METAFOR_CIM_XML_ENCODING : serializer_xml_metafor_cim_v1,
}


def _assert_encoding(encoding):
    """Asserts that the serialization encoding is supported."""
    if not encoding in _serializers:
        raise ValueError('Document encoding is unsupported :: encoding = {0}.'.format(encoding))


def _assert_doc(doc):
    """Asserts that the document is encodable."""    
    rt.assert_doc('doc', doc, "Cannot encode a null document")
    

def _assert_representation(repr):
    """Asserts that the representation is decodable."""
    if repr is None:
        _raise("Documents cannot be decoded from null objects.")


def decode(repr, encoding):
    """Decodes a esdoc_api.lib.pyesdoc document representation.

    :param repr: A document representation (e.g. json).
    :type repr: str

    :param encoding: A document encoding (dict|json|xml|metafor-cim-1-xml).
    :type encoding: str

    :returns: A esdoc_api.lib.pyesdoc document instance.
    :rtype: object

    """
    _assert_representation(repr)
    _assert_encoding(encoding)

    return _serializers[encoding].decode(repr)


def encode(doc, encoding):
    """Encodes a esdoc_api.lib.pyesdoc document instance.

    :param doc: esdoc_api.lib.pyesdoc document instance.
    :type doc: object

    :param encoding: A document encoding (dict|json|xml).
    :type encoding: str

    :returns: A esdoc_api.lib.pyesdoc document representation.
    :rtype: unicode | dict

    """
    _assert_doc(doc)
    _assert_encoding(encoding)

    return _serializers[encoding].encode(doc)
