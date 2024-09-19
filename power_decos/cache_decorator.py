from functools import wraps 

class Cache:
    def __init__(self):
        self.cache = {}

    def clear_cache(self):
        self.cache = {}
    
    def manual_cache(self, func_name: callable, return_value: any, *args, **kwargs):
        key = (func_name, args, frozenset(kwargs.items()))
        self.cache[key] = return_value

    def cache(self, func: callable) -> callable:
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