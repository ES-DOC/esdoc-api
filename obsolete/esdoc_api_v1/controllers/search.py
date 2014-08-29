"""
.. module:: esdoc_api.controllers.query
   :platform: Unix, Windows
   :synopsis: Encapsulates repository query operations.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""

# Module imports.
import itertools

from pylons.decorators import rest
from pylons import response
import pyesdoc

from esdoc_api.lib.api.external_id import get_handler as get_external_id_handler
from esdoc_api.lib.controllers import *
from esdoc_api.lib.utils.http_utils import *
from esdoc_api.lib.utils.xml_utils import *
import esdoc_api.lib.api.search as se
from pyesdoc.db import (
    cache,
    dao,
    models,
    utils
    )
import esdoc_api.lib.utils.runtime as rt
import esdoc_api.lib.controllers.url_validation as uv



# Default URL query parameters.
_default_params = (
    {
        'name' : 'onJSONPLoad',
        'required' : False,
    },
    {
        'name' : 'project',
        'required' : True,
        'whitelist' : lambda : cache.get_names(models.Project),
        'key_formatter' : lambda n : n.lower(),
    },
    {
        'name' : 'timestamp',
        'required' : True,
    },
    {
        'name' : 'searchType',
        'required' : True,
        'whitelist' : lambda : [
            'documentByDRS',
            'documentByExternalID',
            'documentByID',
            'documentByName',
            'documentSummaryByName',
            'se1',
        ],
    },
)

_params_do_defaults_document_by = _default_params + (
    {
        'name' : 'language',
        'required' : True,
        'whitelist' : lambda : cache.get_names(models.DocumentLanguage),
        'key_formatter' : lambda k : k.lower(),
    },
    {
        'name' : 'encoding',
        'required' : True,
        'whitelist' : lambda : cache.get_names(models.DocumentEncoding),
        'key_formatter' : lambda k : k.lower(),
    },
    {
        'name' : 'ontology',
        'required' : True,
        'whitelist' : lambda : cache.get_names(models.DocumentOntology),
        'key_formatter' : lambda k : k.lower(),
    }
)

# URL query parameters for do action.
_params_do = {
    'documentByDRS' : _params_do_defaults_document_by + (
        {
            'name' : 'drsPath',
            'required' : True
        },
    ),
    'documentByExternalID' : _params_do_defaults_document_by + (
        {
            'name' : 'externalID',
            'required' : True,
        },
        {
            'name' : 'externalType',
            'required' : True,
        },
        {
            'name' : 'typeWhiteList',
            'required' : False,
        },
        {
            'name' : 'typeBlackList',
            'required' : False,
        },
    ),
    'documentByID' : _params_do_defaults_document_by + (
        {
            'name' : 'id',
            'required' : True,
        },
        {
            'name' : 'version',
            'required' : True,
        },
    ),
    'documentByName' : _params_do_defaults_document_by + (
        {
            'name' : 'name',
            'required' : True,
        },
        {
            'name' : 'type',
            'required' : True,
        },
        {
            'name' : 'institute',
            'required' : False,
            'whitelist' : lambda : cache.get_names(models.Institute),
            'key_formatter' : lambda k : k.lower(),
        },
    ),
    'documentSummaryByName' : _default_params + (

    ),
    'se1' : _default_params + (
        {
            'name' : 'documentLanguage',
            'required' : True,
            'whitelist' : lambda : cache.get_names(models.DocumentLanguage),
            'key_formatter' : lambda k : k.lower(),
        },
        {
            'name' : 'documentType',
            'required' : True,
            'whitelist' : lambda : cache.get_names(models.DocumentType),
            'key_formatter' : lambda k : k.lower(),
        },
        {
            'name' : 'documentVersion',
            'required' : True,
            'whitelist' : lambda : models.DOCUMENT_VERSIONS
        },
        {
            'name' : 'institute',
            'required' : False,
            'whitelist' : lambda : cache.get_names(models.Institute),
            'key_formatter' : lambda k : k.lower(),
        }
    )
}


# URL query parameters for setup action.
_params_setup = {
    'se1' : (
        {
            'name' : 'onJSONPLoad',
            'required' : False,
        },
        {
            'name' : 'project',
            'required' : False,
            'whitelist' : lambda : cache.get_names(models.Project),
            'key_formatter' : lambda n : n.lower(),
        },
        {
            'name' : 'timestamp',
            'required' : True,
        },
        {
            'name' : 'searchType',
            'required' : True,
            'whitelist' : lambda : [
                'documentByDRS',
                'documentByExternalID',
                'documentByID',
                'documentByName',
                'documentSummaryByName',
                'se1',
            ],
        },
    )
}


def _validate_url_params(params):
    """Helper method to validate url parameters."""
    # Validate search type.
    uv.validate(_default_params[2])

    # Validate other params.
    uv.validate(params[request.params['searchType']])


def _get_se_params():
    """Factory method to derive set of search engine parameters from url."""
    params = {}
    for key in [k for k in request.params if k not in ('onJSONPLoad', 'searchType')]:
        params[key] = request.params[key]

    return params


class SearchController(BaseAPIController):
    """ES-DOC API repository query controller.

    """
    def __before__(self, action, **kwargs):
        """Pre action invocation handler.

        """
        super(SearchController, self).__before__(action, **kwargs)

        # Set common context info.
        self.__set_doc_metainfo()

        # Permit CORS - TODO apply white list from a config file.
        response.headers['Access-Control-Allow-Origin'] = '*'


    def __set_doc_metainfo(self):
        """Assigns document meta-information from incoming http request.

        """
        # Assign values.
        setters = [
            self.__set_doc_project,
            self.__set_doc_institute,
            self.__set_doc_ontology,
            self.__set_doc_encoding,
            self.__set_doc_language
        ]
        for setter in setters:
            setter()


    def __set_doc_project(self):
        """Assigns document project from incoming http request.

        """
        self.project = None if not request.params.has_key('project') else \
                       cache.get_project(request.params['project'])
        self.project_id = None if self.project is None else self.project.ID


    def __set_doc_institute(self):
        """Assigns document institute from incoming http request.

        """
        self.institute = None if not request.params.has_key('institute') else \
                         cache.get_institute(request.params['institute'])
        self.institute_id = None if self.institute is None else self.institute.ID


    def __set_doc_encoding(self):
        """Assigns document encoding from incoming http request.

        """
        self.encoding = None if not request.params.has_key('encoding') else \
                        cache.get_doc_encoding(request.params['encoding'])
        self.encoding_id = None if self.encoding is None else self.encoding.ID
        self.json_encoding = cache.get_doc_encoding('json')
        self.html_encoding = cache.get_doc_encoding('html')
        if self.encoding is None:
            self.encoding = self.json_encoding
            self.encoding_id = self.json_encoding.ID


    def __set_doc_language(self):
        """Assigns document language from incoming http request.

        """
        self.language = None if not request.params.has_key('language') else \
                        cache.get_doc_language(request.params['language'].split('-')[0].lower())
        self.language_id = None if self.language is None else self.language.ID


    def __set_doc_ontology(self):
        """Assigns document ontology from incoming http request.

        """
        self.ontology = None if not request.params.has_key('ontology') else \
                        cache.get_doc_ontology(request.params['ontology'])
        self.ontology_id = None if self.ontology is None else self.ontology.ID


    def __load_representation_set(self, document_set):
        """Loads a document representation set.

        :param document_set: document set being loaded.
        :type document_set: array of documents.

        :returns: array of document representations.
        :rtype: string list

        """
        def load(document):
            return pyesdoc.archive.get(document.UID, document.Version)


        def convert(doc_set):
            result = []
            for doc in doc_set:
                doc = pyesdoc.decode(doc, 'json')
                doc = pyesdoc.extend(doc)
                doc = pyesdoc.encode(doc, self.encoding.Encoding)
                result.append(doc)

            return result

        def convert_to_html(doc_set):
            result = []
            for doc in doc_set:
                doc = pyesdoc.decode(doc, 'json')
                doc = pyesdoc.extend(doc)
                result.append(doc)

            return pyesdoc.encode(result, self.encoding.Encoding)

        # Load representation set.
        result = [] if document_set is None else \
                 [r for r in [load(d) for d in document_set] if r is not None]

        # Convert when necessary.
        if self.encoding == self.json_encoding:
            return result
        elif self.encoding == self.html_encoding:
            return convert_to_html(result)
        else:
            return convert(result)


    def __apply_type_filters(self, ds):
        """Apply white/black type list filters."""
        def apply_type_filter(param):
            type_keys = map(lambda s : s.strip(),
                            request.params[param].upper().split(','))
            is_white_list = True if 'White' in param else False
            def do_filter(memo, d):
                if is_white_list:
                    if d.Type.upper() in type_keys:
                        memo.append(d)
                elif d.Type.upper() not in type_keys:
                    memo.append(d)
                return memo

            return reduce(do_filter, ds, [])

        for param in ['typeBlackList', 'typeWhiteList']:
            if request.params.has_key(param):
                ds = apply_type_filter(param)

        return ds


    def __initialise_ds(self, ds):
        if ds and isinstance(ds, Document):
            return [ds]
        else:
            return []


    def __load(self, load):
        """Loads document representations from repository.

        :param load: Function to load document.
        :type load: Function

        :returns: A list of document representations.
        :rtype: list

        """
        transformers = [
            self.__initialise_ds,
            self.__apply_type_filters,
            self.__load_representation_set
        ]

        return reduce(lambda docs, func : func(docs), transformers, load())


    def __get_documentset_by_id(self):
        """Returns first document set with matching id and version.

        :returns: a collection of document representations.
        :rtype: json list

        """
        def get_id():
            if not request.params.has_key('id'):
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter id is mandatory")

            return request.params['id'].lower()

        def get_version():
            if not request.params.has_key('version'):
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter version is mandatory")
            version = request.params['version'].lower()
            if version not in models.DOCUMENT_VERSIONS:
                try:
                    version = int(version)
                except ValueError:
                    abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter version must be either an integer or one of the string literals 'latest' | '*'.")

            return version

        return self.__load(lambda : dao.get_document(self.project_id,
                                                     get_id(),
                                                     get_version()))


    def __get_documentset_by_name(self):
        """Returns first document set with matching type and name.

        :returns: a collection of document representations.
        :rtype: json list

        """
        def get_type():
            if not request.params.has_key('type'):
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter type is mandatory")

            return request.params['type']


        def get_name():
            if not request.params.has_key('name'):
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter name is mandatory")

            return request.params['name']

        return self.__load(lambda : dao.get_document_by_name(self.project_id,
                                                             get_type(),
                                                             get_name(),
                                                             self.institute_id))


    def __get_documentset_by_drs(self):
        """Returns first document set with matching drs path.

        :returns: a set of document representations.
        :rtype: json list

        """
        def get_drs_path():
            if not request.params.has_key('drsPath'):
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter drsPath is mandatory")
            if len(request.params['drsPath'].split('/')) == 0:
                abort(HTTP_RESPONSE_BAD_REQUEST, "A DRS path must contain at least one key")
            if len(request.params['drsPath'].split('/')) > 8:
                abort(HTTP_RESPONSE_BAD_REQUEST, "A DRS path must consist of a maximum 8 keys")

            return request.params['drsPath']

        def get_drs_keys():
            def is_valid_key(key):
                return len(key) > 0 and \
                       key.upper() != self.project.Name

            return filter(is_valid_key, get_drs_path().split('/'))


        keys = get_drs_keys()
        return self.__load(lambda : dao.get_document_by_drs_keys(self.project_id,
                                                                 keys[0] if len(keys) > 0 else None,
                                                                 keys[1] if len(keys) > 1 else None,
                                                                 keys[2] if len(keys) > 2 else None,
                                                                 keys[3] if len(keys) > 3 else None,
                                                                 keys[4] if len(keys) > 4 else None,
                                                                 keys[5] if len(keys) > 5 else None,
                                                                 keys[6] if len(keys) > 6 else None,
                                                                 keys[7] if len(keys) > 7 else None))



    def __get_documentset_by_external_id(self):
        """Returns first document set with matching external type and id.

        :returns: a collection of document representations.
        :rtype: json list

        """
        def get_type():
            if not request.params.has_key('externalType'):
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter externalType is mandatory")

            return request.params['externalType']

        def get_handler():
            handler = get_external_id_handler(self.project, get_type())
            if handler is None:
                abort(HTTP_RESPONSE_BAD_REQUEST, "External type is unsupported")

            return handler

        def get_id():
            if not request.params.has_key('externalID'):
                abort(HTTP_RESPONSE_BAD_REQUEST, "URL parameter externalID is mandatory")

            handler = get_handler()
            if not handler.is_valid(request.params['externalID']):
                abort(HTTP_RESPONSE_BAD_REQUEST, "External ID is invalid")

            return handler.parse(request.params['externalID'])

        # Load document set.
        handler = get_handler()
        return self.__load(lambda : handler.do_query(self.project, get_id()))


    def __load_results(self):
        """Returns search engine results.

        """
        try:
            searchType = request.params['searchType']
            params = _get_se_params()
            return se.get_results_data(searchType, params)
        except rt.ESDOC_API_Error as e:
            abort(HTTP_RESPONSE_BAD_REQUEST, e.message)


    def __load_setup(self):
        """Returns search engine setup data.

        """
        try:
            return se.get_setup_data(request.params['searchType'])
        except rt.ESDOC_API_Error as err:
            abort(HTTP_RESPONSE_BAD_REQUEST, err.message)


    @rest.restrict('GET')
    def do(self):
        """Executes a document set search against ES-DOC API repository.

        """
        @jsonify
        def as_json(data):
            return data

        def as_html(data):
            return "<div class='esdoc-document-set'>{0}</div>".format(data)

        # Set of handlers.
        handlers = {
            'documentByDRS' : self.__get_documentset_by_drs,
            'documentByID' : self.__get_documentset_by_id,
            'documentByName' : self.__get_documentset_by_name,
            'documentByExternalID' : self.__get_documentset_by_external_id,
            'documentSummaryByName' : self.__load_results,
            'se1' : self.__load_results,
        }

        # Set of formatters.
        formatters = {
            'json': as_json,
            'html': as_html
        }

        # Validate URL query parameters.
        _validate_url_params(_params_do)

        # Set response content type.
        response.content_type = self.get_response_content_type()

        # Get search results.
        results = handlers[request.params['searchType']]()

        # Return in relevant encoding.
        if self.encoding.Encoding in formatters:
            return formatters[self.encoding.Encoding](results)
        else:
            return results


    @rest.restrict('GET')
    @jsonify
    def setup(self):
        """Returns setup data used to configure a UI for searching against ES-DOC API repository.

        :returns: Search engine setup data.
        :rtype: dict

        """
        # Validate URL query parameters.
        _validate_url_params(_params_setup)

        # Set of handlers.
        handlers = {
            'se1' : self.__load_setup,
        }

        # Return handler invocation result.
        return handlers[request.params['searchType']]()