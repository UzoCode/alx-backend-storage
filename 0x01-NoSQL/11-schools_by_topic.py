#!/usr/bin/env python3
"""
Here I learn Python?
"""


def schools_by_topic(mongo_collection, topic):
    """
    make returns of list of school having specific topic

    :param mongo_collection:
    :param topic:
    :return:
    """
    return mongo_collection.find({"topics": topic})
