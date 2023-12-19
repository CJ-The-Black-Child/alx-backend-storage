#!/usr/bin/env python3
""" Module for task 11"""


def schools_by_topic(mongo_collection, topic):
    """
    Returns the list of school having a specific topic
    """
    return list(mongo_collection.find({"topic": topic}))
