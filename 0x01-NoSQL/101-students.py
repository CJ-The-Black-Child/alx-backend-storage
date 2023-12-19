#!/usr/bin/env python3
"""
Module for task 14
"""


def top_students(mongo_collection):
    """
    Returns all students sorted by average score
    """
    stduents = [
        {"$unwind": "$topics"},
        {"$group": {"_id": "$_id",
                    "averageScore": {"$avg": "$topics.score"},
                    "name": {"$first": "$name"}}},
        {"$sort": {"averageScore": -1}}
    ]
    return list(mongo_collection.aggregate(stduents))
