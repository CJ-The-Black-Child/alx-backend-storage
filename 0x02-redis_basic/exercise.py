#!/usr/bin/env python3
"""
Using Redis NoSQL data storage
"""
import uuid
import redis
from functools import wraps
from typing import Any, Callable, Optional, Union


class Cache:
    """
    Represents an object for storing data in a Redis data storage.
    """
    def __init__(self) -> None:
        """
        Initializes a Cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """
        Tracks the number of calls made to a method in a Cache class.
        """
        @wraps(method)
        def invoker(self, *args, **kwargs) -> Any:
            """
            Invokes the given method after incrementing its call counter.
            """
            self._redis.incr(method.__qualname__)
            return method(self, *args, **kwargs)
        return invoker

    @staticmethod
    def call_history(method: Callable) -> Callable:
        """
        Tracks the call details of a method in a Cache class.
        """
        @wraps(method)
        def invoker(self, *args, **kwargs) -> Any:
            """
            Returns the method's output after storing its inputs and output.
            """
            self._redis.rpush(f"{method.__qualname__}:inputs", str(args))
            result = method(self, *args, **kwargs)
            self._redis.rpush(f"{method.__qualname__}:outputs", str(result))
            return result
        return invoker

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores a value in a Redis data storage and returns the key.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
        self,
        key: str,
        fn: Optional[Callable] = None
    ) -> Union[str, bytes, int, float]:
        """
        Retrieves a value from a Redis data storage.
        """
        data = self._redis.get(key)
        return fn(data) if fn else data

    def get_str(self, key: str) -> str:
        """
        Retrieves a string value from a Redis data storage.
        """
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """
        Retrieves an integer value from a Redis data storage.
        """
        return self.get(key, int)

    @staticmethod
    def replay(method: Callable) -> None:
        """
        Displays the call history of a Cache class' method.
        """
        redis_store = method.__self__._redis
        method_name = method.__qualname__
        inputs = redis_store.lrange(f"{method_name}:inputs", 0, -1)
        outputs = redis_store.lrange(f"{method_name}:outputs", 0, -1)
        print(f"{method_name} was called {len(inputs)} times:")
        for inp, out in zip(inputs, outputs):
            print(
                f"{method_name}{inp.decode('utf-8')} -> {out.decode('utf-8')}"
            )
