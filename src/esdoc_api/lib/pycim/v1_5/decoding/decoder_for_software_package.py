"""A set of cim 1.5 decodings.

CIM CODE GENERATOR :: Code generated @ 2013-01-30 15:45:18.451308.
"""

# Module imports.
from esdoc_api.lib.pycim.core.decoding.cim_decoder_xml_utils import *
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_activity_package import *
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_data_package import *
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_grids_package import *
from esdoc_api.lib.pycim.v1_5.decoding.decoder_for_shared_package import *
from esdoc_api.lib.pycim.v1_5.types.software import *


# Module exports.
__all__ = [
    "decode_component", 
    "decode_component_language", 
    "decode_component_language_property", 
    "decode_component_property", 
    "decode_composition", 
    "decode_connection", 
    "decode_connection_endpoint", 
    "decode_connection_property", 
    "decode_coupling", 
    "decode_coupling_endpoint", 
    "decode_coupling_property", 
    "decode_deployment", 
    "decode_entry_point", 
    "decode_model_component", 
    "decode_parallelisation", 
    "decode_processor_component", 
    "decode_rank", 
    "decode_spatial_regridding", 
    "decode_spatial_regridding_property", 
    "decode_spatial_regridding_user_method", 
    "decode_time_lag", 
    "decode_time_transformation", 
    "decode_timing"
]


# Module provenance info.
__author__="Mark Morgan"
__copyright__ = "Copyright 2013 - Institut Pierre Simon Laplace."
__date__ ="2013-01-30 15:45:18.451308"
__license__ = "GPL"
__version__ = "1.5.0"
__maintainer__ = "Mark Morgan"
__email__ = "momipsl@ipsl.jussieu.fr"
__status__ = "Production"


def decode_component(xml, nsmap):
    """Decodes a component instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('children', True, decode_model_component, 'child::cim:childComponent/cim:modelComponent'),
        ('children', True, decode_processor_component, 'child::cim:childComponent/cim:processorComponent'),
        ('citation_list', True, decode_citation, 'child::cim:citation'),
        ('citations', True, decode_citation, 'child::cim:citation'),
        ('description', False, 'str', 'child::cim:description'),
        ('language', False, decode_component_language, 'child::cim:componentLanguage'),
        ('long_name', False, 'str', 'child::cim:longName'),
        ('properties', True, decode_component_property, 'child::cim:componentProperties/cim:componentProperty'),
        ('properties', True, decode_component_property, 'child::cim:scientificProperties/cim:componentProperty'),
        ('properties', True, decode_component_property, 'child::cim:numericalProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:componentProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:scientificProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:numericalProperties/cim:componentProperty'),
        ('release_date', False, 'datetime', 'child::cim:releaseDate'),
        ('responsible_parties', True, decode_responsible_party, 'child::cim:responsibleParty'),
        ('responsible_party_list', True, decode_responsible_party, 'child::cim:responsibleParty'),
        ('short_name', False, 'str', 'child::cim:shortName'),
    ]

    return set_attributes(Component(), xml, nsmap, decodings)


def decode_component_language(xml, nsmap):
    """Decodes a component language instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('name', False, 'str', 'child::cim:name'),
    ]

    return set_attributes(ComponentLanguage(), xml, nsmap, decodings)


def decode_component_language_property(xml, nsmap):
    """Decodes a component language property instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('name', False, 'str', 'child::cim:name'),
        ('value', False, 'str', 'child::cim:value'),
    ]

    return set_attributes(ComponentLanguageProperty(), xml, nsmap, decodings)


def decode_component_property(xml, nsmap):
    """Decodes a component property instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('children', True, decode_component_property, 'child::cim:componentProperty'),
        ('citations', True, decode_citation, 'child::cim:citation'),
        ('description', False, 'str', 'child::cim:description'),
        ('intent', False, 'str', 'self::cim:componentProperty/@intent'),
        ('is_represented', False, 'bool', 'self::cim:componentProperty/@represented'),
        ('long_name', False, 'str', 'child::cim:longName'),
        ('short_name', False, 'str', 'child::cim:shortName'),
        ('standard_names', True, 'str', 'child::cim:standardName/@value'),
        ('units', False, 'str', 'child::cim:units/@value'),
        ('values', True, 'str', 'child::cim:value'),
    ]

    return set_attributes(ComponentProperty(), xml, nsmap, decodings)


def decode_composition(xml, nsmap):
    """Decodes a composition instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
    ]

    return set_attributes(Composition(), xml, nsmap, decodings)


def decode_connection(xml, nsmap):
    """Decodes a connection instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('priming', False, decode_data_object, 'child::cim:priming/cim:priming/cim:dataObject'),
        ('priming', False, decode_data_content, 'child::cim:priming/cim:priming/cim:dataContent'),
        ('priming', False, decode_component_property, 'child::cim:priming/cim:priming/cim:componentProperty'),
        ('priming', False, decode_model_component, 'child::cim:priming/cim:priming/cim:softwareComponent'),
        ('priming', False, decode_processor_component, 'child::cim:priming/cim:priming/cim:softwareComponent'),
        ('priming_reference', False, decode_cim_reference, 'child::cim:priming/cim:reference'),
        ('properties', True, decode_connection_property, 'child::cim:connectionProperty'),
        ('sources', True, decode_connection_endpoint, 'child::cim:connectionSource'),
        ('spatial_regridding', True, decode_spatial_regridding, 'child::cim:spatialRegridding'),
        ('target', False, decode_connection_endpoint, 'child::cim:connectionTarget'),
        ('time_lag', False, 'str', 'child::cim:timeLag'),
        ('time_profile', False, decode_timing, 'child::cim:timeProfile'),
        ('time_transformation', False, decode_time_transformation, 'child::cim:timeTransformation'),
        ('transformers', True, decode_processor_component, 'child::cim:transformer/cim:processorComponent'),
        ('transformers_references', True, decode_cim_reference, 'child::cim:transformer/cim:reference'),
        ('type', False, 'str', 'child::cim:type/@value'),
    ]

    return set_attributes(Connection(), xml, nsmap, decodings)


def decode_connection_endpoint(xml, nsmap):
    """Decodes a connection endpoint instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('data_source', False, decode_data_object, 'child::cim:dataSource/cim:dataSource/cim:dataObject'),
        ('data_source', False, decode_data_content, 'child::cim:dataSource/cim:dataSource/cim:dataContent'),
        ('data_source', False, decode_component_property, 'child::cim:dataSource/cim:dataSource/cim:componentProperty'),
        ('data_source', False, decode_model_component, 'child::cim:dataSource/cim:dataSource/cim:softwareComponent'),
        ('data_source', False, decode_processor_component, 'child::cim:dataSource/cim:dataSource/cim:softwareComponent'),
        ('data_source_reference', False, decode_cim_reference, 'child::cim:dataSource/cim:reference'),
        ('instance_id', False, 'str', 'child::cim:instanceID'),
        ('properties', True, decode_connection_property, 'child::cim:connectionProperty'),
    ]

    return set_attributes(ConnectionEndpoint(), xml, nsmap, decodings)


def decode_connection_property(xml, nsmap):
    """Decodes a connection property instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('name', False, 'str', 'child::cim:name'),
        ('value', False, 'str', 'child::cim:value'),
    ]

    return set_attributes(ConnectionProperty(), xml, nsmap, decodings)


def decode_coupling(xml, nsmap):
    """Decodes a coupling instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('connections', True, decode_connection, 'child::cim:connection'),
        ('description', False, 'str', 'child::cim:description'),
        ('is_fully_specified', False, 'bool', '@fullySpecified'),
        ('priming', False, decode_data_object, 'child::cim:priming/cim:priming/cim:dataObject'),
        ('priming', False, decode_data_content, 'child::cim:priming/cim:priming/cim:dataContent'),
        ('priming', False, decode_component_property, 'child::cim:priming/cim:priming/cim:componentProperty'),
        ('priming', False, decode_model_component, 'child::cim:priming/cim:priming/cim:softwareComponent'),
        ('priming', False, decode_processor_component, 'child::cim:priming/cim:priming/cim:softwareComponent'),
        ('priming_reference', False, decode_cim_reference, 'child::cim:priming/cim:reference'),
        ('properties', True, decode_coupling_property, 'child::cim:couplingProperty'),
        ('purpose', False, 'str', '@purpose'),
        ('sources', True, decode_coupling_endpoint, 'child::cim:couplingSource'),
        ('spatial_regriddings', True, decode_spatial_regridding, 'child::cim:spatialRegridding'),
        ('target', False, decode_coupling_endpoint, 'child::cim:couplingTarget'),
        ('time_lag', False, decode_time_lag, 'child::cim:timeLag'),
        ('time_profile', False, decode_timing, 'child::cim:timeProfile'),
        ('time_transformation', False, decode_time_transformation, 'child::cim:timeTransformation'),
        ('transformers', True, decode_processor_component, 'child::cim:transformer/cim:processorComponent'),
        ('transformers_references', True, decode_cim_reference, 'child::cim:transformer/cim:reference'),
        ('type', False, 'str', 'child::cim:type/@value'),
    ]

    return set_attributes(Coupling(), xml, nsmap, decodings)


def decode_coupling_endpoint(xml, nsmap):
    """Decodes a coupling endpoint instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('data_source', False, decode_data_object, 'child::cim:dataSource/cim:dataSource/cim:dataObject'),
        ('data_source', False, decode_data_content, 'child::cim:dataSource/cim:dataSource/cim:dataContent'),
        ('data_source', False, decode_component_property, 'child::cim:dataSource/cim:dataSource/cim:componentProperty'),
        ('data_source', False, decode_model_component, 'child::cim:dataSource/cim:dataSource/cim:softwareComponent'),
        ('data_source', False, decode_processor_component, 'child::cim:dataSource/cim:dataSource/cim:softwareComponent'),
        ('data_source_reference', False, decode_cim_reference, 'child::cim:dataSource/cim:reference'),
        ('instance_id', False, 'str', 'child::cim:instanceID'),
        ('properties', True, decode_coupling_property, 'child::cim:couplingProperty'),
    ]

    return set_attributes(CouplingEndpoint(), xml, nsmap, decodings)


def decode_coupling_property(xml, nsmap):
    """Decodes a coupling property instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('name', False, 'str', 'child::cim:name'),
        ('value', False, 'str', 'child::cim:value'),
    ]

    return set_attributes(CouplingProperty(), xml, nsmap, decodings)


def decode_deployment(xml, nsmap):
    """Decodes a deployment instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('deployment_date', False, 'datetime', 'child::cim:deploymentDate'),
        ('description', False, 'str', 'child::cim:description'),
        ('executable_arguments', True, 'str', 'child::cim:executableArgument'),
        ('executable_name', False, 'str', 'child::cim:executableName'),
        ('parallelisation', False, decode_parallelisation, 'child::cim:parallelisation'),
        ('platform', False, decode_platform, 'child::cim:platform/cim:platform'),
        ('platform_reference', False, decode_cim_reference, 'child::cim:platform/cim:reference'),
    ]

    return set_attributes(Deployment(), xml, nsmap, decodings)


def decode_entry_point(xml, nsmap):
    """Decodes a entry point instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
    ]

    return set_attributes(EntryPoint(), xml, nsmap, decodings)


def decode_model_component(xml, nsmap):
    """Decodes a model component instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('children', True, decode_model_component, 'child::cim:childComponent/cim:modelComponent'),
        ('children', True, decode_processor_component, 'child::cim:childComponent/cim:processorComponent'),
        ('cim_info', False, decode_cim_info, 'self::cim:modelComponent'),
        ('citation_list', True, decode_citation, 'child::cim:citation'),
        ('citations', True, decode_citation, 'child::cim:citation'),
        ('description', False, 'str', 'child::cim:description'),
        ('language', False, decode_component_language, 'child::cim:componentLanguage'),
        ('long_name', False, 'str', 'child::cim:longName'),
        ('properties', True, decode_component_property, 'child::cim:componentProperties/cim:componentProperty'),
        ('properties', True, decode_component_property, 'child::cim:scientificProperties/cim:componentProperty'),
        ('properties', True, decode_component_property, 'child::cim:numericalProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:componentProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:scientificProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:numericalProperties/cim:componentProperty'),
        ('release_date', False, 'datetime', 'child::cim:releaseDate'),
        ('responsible_parties', True, decode_responsible_party, 'child::cim:responsibleParty'),
        ('responsible_party_list', True, decode_responsible_party, 'child::cim:responsibleParty'),
        ('short_name', False, 'str', 'child::cim:shortName'),
        ('type', False, 'str', 'child::cim:type[1]/@value'),
        ('types', True, 'str', 'child::cim:type/@value'),
    ]

    return set_attributes(ModelComponent(), xml, nsmap, decodings)


def decode_parallelisation(xml, nsmap):
    """Decodes a parallelisation instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('processes', False, 'int', 'child::cim:processes'),
        ('ranks', True, decode_rank, 'child::cim:rank'),
    ]

    return set_attributes(Parallelisation(), xml, nsmap, decodings)


def decode_processor_component(xml, nsmap):
    """Decodes a processor component instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('children', True, decode_model_component, 'child::cim:childComponent/cim:modelComponent'),
        ('children', True, decode_processor_component, 'child::cim:childComponent/cim:processorComponent'),
        ('cim_info', False, decode_cim_info, 'self::cim:modelComponent'),
        ('citation_list', True, decode_citation, 'child::cim:citation'),
        ('citations', True, decode_citation, 'child::cim:citation'),
        ('description', False, 'str', 'child::cim:description'),
        ('language', False, decode_component_language, 'child::cim:componentLanguage'),
        ('long_name', False, 'str', 'child::cim:longName'),
        ('properties', True, decode_component_property, 'child::cim:componentProperties/cim:componentProperty'),
        ('properties', True, decode_component_property, 'child::cim:scientificProperties/cim:componentProperty'),
        ('properties', True, decode_component_property, 'child::cim:numericalProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:componentProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:scientificProperties/cim:componentProperty'),
        ('property_tree', True, decode_component_property, 'child::cim:numericalProperties/cim:componentProperty'),
        ('release_date', False, 'datetime', 'child::cim:releaseDate'),
        ('responsible_parties', True, decode_responsible_party, 'child::cim:responsibleParty'),
        ('responsible_party_list', True, decode_responsible_party, 'child::cim:responsibleParty'),
        ('short_name', False, 'str', 'child::cim:shortName'),
    ]

    return set_attributes(ProcessorComponent(), xml, nsmap, decodings)


def decode_rank(xml, nsmap):
    """Decodes a rank instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('increment', False, 'int', 'child::cim:rankIncrement'),
        ('max', False, 'int', 'child::cim:rankMax'),
        ('min', False, 'int', 'child::cim:rankMin'),
        ('value', False, 'int', 'child::cim:rankValue'),
    ]

    return set_attributes(Rank(), xml, nsmap, decodings)


def decode_spatial_regridding(xml, nsmap):
    """Decodes a spatial regridding instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('dimension', False, 'str', 'child::cim:spatialRegriddingDimension'),
        ('properties', True, decode_spatial_regridding_property, 'child::cim:spatialRegriddingProperty'),
        ('standard_method', False, 'str', 'child::cim:spatialRegriddingStandardMethod'),
        ('user_method', False, decode_spatial_regridding_user_method, 'child::cim:spatialRegriddingUserMethod'),
    ]

    return set_attributes(SpatialRegridding(), xml, nsmap, decodings)


def decode_spatial_regridding_property(xml, nsmap):
    """Decodes a spatial regridding property instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('name', False, 'str', 'child::cim:name'),
        ('value', False, 'str', 'child::cim:value'),
    ]

    return set_attributes(SpatialRegriddingProperty(), xml, nsmap, decodings)


def decode_spatial_regridding_user_method(xml, nsmap):
    """Decodes a spatial regridding user method instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('file', False, decode_data_object, 'child::cim:file/cim:dataObject'),
        ('file_reference', False, decode_cim_reference, 'child::cim:file/cim:reference'),
        ('name', False, 'str', 'child::cim:name'),
    ]

    return set_attributes(SpatialRegriddingUserMethod(), xml, nsmap, decodings)


def decode_time_lag(xml, nsmap):
    """Decodes a time lag instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('units', False, 'str', '@units'),
        ('value', False, 'int', 'child::cim:value'),
    ]

    return set_attributes(TimeLag(), xml, nsmap, decodings)


def decode_time_transformation(xml, nsmap):
    """Decodes a time transformation instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('description', False, 'str', 'child::cim:description'),
        ('mapping_type', False, 'str', 'child::cim:mappingType/@value'),
    ]

    return set_attributes(TimeTransformation(), xml, nsmap, decodings)


def decode_timing(xml, nsmap):
    """Decodes a timing instance from xml.

    Keyword arguments:
    xml -- etree xml element from which entity is to be decoded.
    nsmap -- set of xml namespace mappings.

    """
    decodings = [
        ('end', False, 'datetime', 'child::cim:end'),
        ('is_variable_rate', False, 'bool', '@variableRate'),
        ('rate', False, 'int', 'child::cim:rate'),
        ('start', False, 'datetime', 'child::cim:start'),
        ('units', False, 'str', '@units'),
    ]

    return set_attributes(Timing(), xml, nsmap, decodings)


