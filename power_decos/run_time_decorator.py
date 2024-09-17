"""
Module containing the retry decorator

**Decorators**:
    - **get_time**: Wrapps Function and returns execution time
"""

import logging
from time import perf_counter
from functools import wraps

# Initialize logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

def get_time(func: callable) -> callable:
    """
    Wrapps Function and returns execution time

    **Prints:**
    - run_time (float): -> the time of the execution of a Function

    :return: Callable[..., Any]: The decorated function that prints its execution time.

    :note:
        - This decorator will print the execution time regardless of whether the function
          raises an exception or not.
    """
    @wraps(func)
    def wrapper(*args, **kwargs) -> any:

        start_time: float = perf_counter()
        result: any = func(*args, **kwargs)
        end_time: float = perf_counter()

        logger.info(f"Function {func.__name__} took {end_time - start_time:.3f} seconds to execute")

        return result

    return wrapper
