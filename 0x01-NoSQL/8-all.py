#!/usr/bin/env python3
"""
makes list all documents in Python
"""


def list_all(mongo_collection):
    """
    A lists of all documents in a collection

    :param mongo_collection:
    :return:
    """
    return mongo_collection.find()
