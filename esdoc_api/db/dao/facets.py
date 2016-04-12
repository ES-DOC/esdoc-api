# -*- coding: utf-8 -*-
"""
.. module:: facets.py
   :platform: Unix
   :synopsis: Data access operations across facets domain space.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
from esdoc_api.db.models import (
    Node,
    NodeField,
)
from esdoc_api.db import session



def get_node(project, type_of, field):
    """Returns a facet node.

    :param str project: Project with which a node is associated.
    :param str type_of: Node type.
    :param str field: Node field.

    :returns: A facet node.
    :rtype: models.Node

    """
    qry = session.query(Node)

    if project is not None:
        qry = qry.filter(Node.project == project)
    if type_of is not None:
        qry = qry.filter(Node.type_of == str(type_of))
    if field is not None:
        qry = qry.filter(Node.field == field)

    return qry.first()


def get_node_count(project=None, type_of=None):
    """Returns a facet node count.

    :param str project: Project with which a node is associated.
    :param str type_of: Node type.

    :returns: A facet node count.
    :rtype: int

    """
    qry = session.query(Node)

    if project is not None:
        qry = qry.filter(Node.project == project)
    if type_of is not None:
        qry = qry.filter(Node.type_of == str(type_of))

    return qry.count()


def get_node_field(text):
    """Returns a facet field value.

    :param str text: Field text.

    :returns: A facet node field.
    :rtype: models.NodeField

    """
    qry = session.query(NodeField)

    qry = qry.filter(NodeField.text == text)

    return qry.first()


def get_node_value(text):
    """Returns a facet node value.

    :param str text: Value of associated facet.

    :returns: A facet node value.
    :rtype: models.NodeValue

    """
    qry = session.query(NodeValue)

    qry = qry.filter(NodeValue.text == text)

    return qry.first()


def get_node_value_set(project=None, type_of=None):
    """Returns set of facet node values filtered by project id.

    :param str project: Project with which facet node values are associated.

    :returns: Set of facet node values.
    :rtype: list

    """
    qry = session.query(NodeValue)

    return qry.all()


def get_node_set(project=None):
    """Returns set of facet nodes filtered by project id.

    :param str project: Project with which facet nodes are associated.

    :returns: Set of facet nodes.
    :rtype: list

    """
    qry = session.query(Node)
    if project is not None:
        qry = qry.filter(Node.project == project)

    return qry.all()


def get_node_field_set(project=None, type_of=None):
    """Returns set of facet nodes filtered by project id.

    :param str project: Project with which facet nodes are associated.

    :returns: Set of facet nodes.
    :rtype: list

    """
    qry = session.query(NodeField)
    if project:
        qry = qry.filter(NodeField.project == project)
    if type_of:
        qry = qry.filter(NodeField.type_of == str(type_of))

    return qry.all()


def get_node_combination(project, type_of, vector):
    """Returns a facet combination.

    :param str project: Project with which a facet combination is associated.
    :param str type_of: Facet combination type.
    :param str vector: Facet combination vector.

    :returns: A facet combination.
    :rtype: models.NodeCombination

    """
    qry = session.query(NodeCombination)
    qry = qry.filter(NodeCombination.project == project)
    qry = qry.filter(NodeCombination.type_of == str(type_of))
    qry = qry.filter(NodeCombination.combination == vector)

    return qry.first()


def get_node_combination_set(project):
    """Returns a facet combination set.

    :param str project: Project with which a facet combination set is associated.

    :returns: A facet combination set.
    :rtype: list

    """
    qry = session.query(NodeCombination)
    qry = qry.filter(NodeCombination.project == project)

    return qry.all()
