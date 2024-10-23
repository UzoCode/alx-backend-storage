#!/usr/bin/env python3
"""
make changes to school topics
"""


def update_topics(mongo_collection, name, topics):
    """
    make changess to all topics of a school
     document based on the name

    :param mongo_collection:
    :param name:
    :param topics:
    :return:
    """
    mongo_collection.update_many({"name": name}, {"$set": {"topics": topics}})
