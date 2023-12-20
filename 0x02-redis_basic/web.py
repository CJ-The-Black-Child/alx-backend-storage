#!/usr/bin/env python3
"""
Redis Module
"""
import redis
import requests
from functools import wraps
from typing import Callable


class WebPage:
    """
    Represents an object for storing webpage data in a Redis data storage.
    """
    def __init__(self) -> None:
        """
        Initializes a WebPage instance.
        """
        self._redis = redis.Redis()

    def count_requests(method: Callable) -> Callable:
        """
        Decorator for counting the number of requests made to a URL.
        """
        @wraps(method)
        def wrapper(self, url: str) -> str:
            """
            Wrapper for decorator. It checks if the HTML content of
            the URL is cached in Redis. If it is, it returns the cached
            content. If not, it sends a request to the URL, stores the HTML
            content in Redis, and returns the content.
            """
            self._redis.incr(f"count:{url}")
            cached_html = self._redis.get(f"cached:{url}")
            if cached_html:
                return cached_html.decode('utf-8')
            html = method(self, url)
            self._redis.setex(f"cached:{url}", 10, html)
            return html
        return wrapper

    @count_requests
    def get_page(self, url: str) -> str:
        """
        Sends a request to a URL and returns the HTML content.
        """
        response = requests.get(url)
        return response.text
