#!/usr/bin/env python3
"""
The Redis module
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    A system that counts number of
    times the methods of Cache class are called.
    :param method:
    :return:
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Wraps
        :param self:
        :param args:
        :param kwargs:
        :return:
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Adds its input parameters to a list
    in redis, then stores its output into another list.
    :param method:
    :return:
    """
    key = method.__qualname__
    i = "".join([key, ":inputs"])
    o = "".join([key, ":outputs"])

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ The Wrapper """
        self._redis.rpush(i, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(o, str(res))
        return res

    return wrapper


class Cache:
    """
    The Cache redis class
    """

    def __init__(self):
        """
        constructor for the redis model
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Generates a random key (e.g. using uuid),
         stores the input data in Redis using the
          random key then return the key.
        :param data:
        :return:
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) \
            -> UnionOfTypes:
        """
        Converts data back
        to desired format
        :param key:
        :param fn:
        :return:
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def get_int(self: bytes) -> int:
        """Gets number"""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """Gets string"""
        return self.decode("utf-8")
