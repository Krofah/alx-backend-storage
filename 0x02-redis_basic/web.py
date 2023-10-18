#!/usr/bin/env python3
"""
web cache and tracker
"""
import requests
import redis
from functools import wraps

store = redis.Redis()


def count_url_access(func):
    """ Decorator counting how many times a URL is accessed """
    @wraps(func)
    def wrapper(url):
        count_key = f"count:{url}"
        store.incr(count_key)
        return func(url)
    return wrapper


def cache_result(func):
    """ Decorator caching the result with an expiration time of 10 seconds """
    @wraps(func)
    def wrapper(url):
        cached_key = f"cached:{url}"
        cached_data = store.get(cached_key)
        if cached_data:
            return cached_data.decode("utf-8")

        result = func(url)
        store.set(cached_key, result)
        store.expire(cached_key, 10)
        return result
    return wrapper


@count_url_access
@cache_result
def get_page(url: str) -> str:
    """ Returns HTML content of a URL """
    res = requests.get(url)
    return res.text

