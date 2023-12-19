#!/usr/bin/env python3
""" Module for task 10 """


def update_topics(mongo_collection, name, topics):
    """
    Changes all topics pf a school document based on the name.
    """
    return mongo_collection.update_many(
        {'name': name}, {'$set': {'topics': topics}}
    )
