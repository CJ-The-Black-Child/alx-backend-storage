#!/usr/bin/env python3
"""
Redis Module
"""
import redis
import requests
from functools import wraps
from typing import Callable


redis_ = redis.Redis()


def count_requests(method: Callable) -> Callable:
    """
    Decorator for counting the number of requests made to a URL.
    """
    @wraps(method)
    def wrapper(url: str) -> str:
        """
        Wrapper for decorator. It checks if the HTML content of
        the URL is cached in Redis. If it is, it returns the cached
        content. If not, it sends a request to the URL, stores the HTML
        content in Redis, and returns the content.
        """
        redis_.incr(f"count:{url}")
        cached_html = redis_.get(f"cached:{url}")
        if cached_html:
            return cached_html.decode('utf-8')
        html = method(url)
        redis_.setex(f"cached:{url}", 10, html)
        return html
    return wrapper


@count_requests
def get_page(url: str) -> str:
    """
    Sends a request to a URL and returns the HTML content.
    """
    response = requests.get(url)
    return response.text
