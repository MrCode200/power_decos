"""
cache_module
-------------

This module provides a simple caching mechanism for function results.
It includes a `Cache` class that can be used to cache and retrieve
function results, improving performance for expensive or frequently
called functions.

Usage:
    Instantiate the Cache class and decorate functions with the
    `@cache` decorator to enable caching.
"""
from functools import wraps 

class Cache:
    """A simple caching mechanism for storing and retrieving function results.

    This class provides a way to cache the results of function calls, 
    improving performance for expensive or frequently called functions.

    :ivar cache: Saved outpust to tuple(func.__name, args, frozenset(kwargs.item()))
    """
    def __init__(self):
        self.cache = {}

    def clear_cache(self):
        """Clear the cache.

        Resets the cache to an empty state, removing all stored results.
        """
        self.cache = {}
    
    def manual_cache(self, func_name: callable, return_value: any, *args, **kwargs):
        """Manually add a result to the cache.

        :param func_name: The name of the function whose result is being cached.
        :param return_value: The result to cache.
        :param args: Positional arguments used to generate the cache key.
        :param kwargs: Keyword arguments used to generate the cache key.
        """
        key = (func_name, args, frozenset(kwargs.items()))
        self.cache[key] = return_value

    def cache(self, func: callable) -> callable:
        """Decorator to cache the result of a function call.

        If the function is called with the same arguments, the cached 
        result will be returned instead of calling the function again.

        :param func: The function to be cached.
        :return: The wrapper function that handles caching.
        """
        @wraps(func)
        def wrapper(*args, **kwargs) -> any:
            key = (func.__name__, args, frozenset(kwargs.items()))

            if key in self.cache:
                return self.cache[key]
            else:
                result = func(args, kwargs)

            self.cache[key] = result
            return result
        
        return wrapper