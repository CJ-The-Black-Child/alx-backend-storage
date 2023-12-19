#!/usr/bin/env python3
""" Module for task 15 """
from pymongo import MongoClient


def print_nginx_request_logs(nginx_collection):
    """ Prints stats about Nginx request logs """
    print(f"{nginx_collection.count_documents({})} logs")
    print("Methods:")
    methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    for method in methods:
        req_count = len(list(nginx_collection.find({'method': method})))
        print(f"\tmethod {method}: {req_count}")
    status_checks_count = len(list(
        nginx_collection.find({'method': 'GET', 'path': '/status'}))
    )
    print(f"{status_checks_count} status check")


def print_top_ips(nginx_collection):
    """ Prints statistics about the top 10 HTTP IPs in a collection."""
    print("IPs:")
    ips = nginx_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
    ])
    for ip in ips:
        print(f"\t{ip['_id']}: {ip['count']}")


def run():
    """Provides some stats about Nginx logs stored in MongoDB."""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx
    print_nginx_request_logs(nginx_collection)
    print_top_ips(nginx_collection)


if __name__ == "__main__":
    run()
