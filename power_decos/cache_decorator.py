"""
cache_module
-------------

This module provides a simple caching mechanism for function results.
It includes a `Cache` class that can be used to cache and retrieve
function results, improving performance for expensive or frequently
called functions.

cls `Cache`:
    - `clear_cache()`: Clears the cache, resetting it to an empty state.
    - `manual_cache(func_name: callable, return_value: any, *args, **kwargs)`: Manually adds a result to the cache.
    - `cache(func: callable)`: Decorator that caches the result of a function call.
    - `get_cached_value(func_name: callable, compare_all: bool = True, *args, **kwargs)`: Retrieve cached results based on function name and optionally arguments.

Usage:
    Instantiate the Cache class and decorate functions with the
    `@cache` decorator to enable caching.
"""
from functools import wraps

class Cache:
    """A simple caching mechanism for storing and retrieving function results.

    This class provides a way to cache the results of function calls, 
    improving performance for expensive or frequently called functions.

    :ivar cache: Saved output to tuple(func.__name, args, frozenset(kwargs.item()))
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

    def get_cached_value(self, func_name: callable, *args,  compare_all: bool = True, **kwargs) -> any:
        """
        Retrieve cached results based on function name and optionally arguments.

        This method returns cached values for a function based on the specified
        `func_name`, `args`, and `kwargs`. It can either look for an exact match
        or allow for partial matches depending on the `compare_all` flag.

        :param func_name: The name of the function whose result is being retrieved.

        :keyword compare_all: If True, requires an exact match of `func_name`, `args`, and `kwargs`.
                            If False, allows partial matches where `args` and/or `kwargs` can be omitted.

        :param args: Positional arguments used to generate the cache key.
                     If provided, they are used for partial matching when `compare_all` is False.

        :param kwargs: Keyword arguments used to generate the cache key.
                       If provided, they are used for partial matching when `compare_all` is False.
        Returns:
        --------

        1. A single cached result if `compare_all` is True and an exact match is found.

        2. A list of cached results if `compare_all` is False and partial matches are found.

        3. None if no match is found.
        """
        return (self.cache.get((func_name, args, frozenset(kwargs.items())), None)
                if compare_all
                else [result for key, result in self.cache.items()
                      if key[0] == func_name
                      and (args == key[1] or not args)
                      and (frozenset(kwargs.items()) == key[2] or not kwargs)])


    def cache_func(self, func: callable) -> callable:
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
                result = func(*args, **kwargs)

            self.cache[key] = result
            return result
        
        return wrapper