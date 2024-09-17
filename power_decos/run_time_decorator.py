"""
A module containing the `get_time` decorator for measuring and logging the execution time of functions.

Decorators
==========

- `get_time`: Measures the execution time of a function and logs the duration.

Functions
=========

- `get_time`: The main decorator that calculates the time a function takes to execute.

    - It prints and logs the time taken by the decorated function.
    - The execution time is logged regardless of whether the function raises an exception or not.

Exception classes
=================

This module does not define any specific exception classes.

How To Use This Module
======================

1. Import it: ``import time_decorator`` or ``from time_decorator import get_time``.

2. Use the `get_time` decorator to measure the execution time of a function:

       @get_time
       def my_function():
           # function code
           pass

3. The execution time will be logged with a message indicating how long the function took.

Example
=======

```python
from time_decorator import get_time

@get_time
def slow_function():
    # Code that takes time to run
    pass

slow_function()
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
