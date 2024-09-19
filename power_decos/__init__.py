"""
Package full of utility decorators

**Decorators**:

- `retry(num_of_retries=3, interval=1)`: Retries a function upon failure for a specified number of times, with a delay between attempts.

- `get_time()`: Measures and prints the execution time of the decorated function.

- `log_decorator` (cls LogManager):
    - `log_init()`: Initializes and configures how logging data should be handled (e.g., terminal, file, JSON).
    - `log_func()`: Logs the entry, exit, and any exceptions of a function to `.jsonl` or `.log` files.
    - `log_info(message: str)`: Logs custom informational messages to `.jsonl` or `.log` files.

- `cache_decorator` (cls Cache):
    - `clear_cache()`: Clears the cache, resetting it to an empty state.
    - `manual_cache(func_name: callable, return_value: any, *args, **kwargs)`: Manually adds a result to the cache.
    - `cache(func: callable)`: Decorator that caches the result of a function call.
    - `get_cached_value(func_name: callable, compare_all: bool = True, *args, **kwargs)` : Retrieve cached results based on function name and optionally arguments.

This module provides easy-to-use decorators for common tasks like retrying failed operations, measuring execution time, structured logging, and result caching.

**Params**:
- __version__: The version of the package.
- __author__: The author of the package.
"""

# still need to work on the docstring

__version__ = "1.0.0"
__author__ = "MrCode200"

from .retry_decorator import retry
from .run_time_decorator import get_time
from .log_decorator import LoggerManager
from .cache_decorator import Cache

__all__ = ["retry", "get_time", "LoggerManager", "Cache"]
