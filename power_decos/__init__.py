"""
Package full of decorator utils

*Decorators:*

- retry(num_of_retries=3, interval=1) : reexecutes function

- get_time() : prints execution time of function

- log_decorator :
    - log_init() : init and changes how data should be logged
    - log_func() : logs exc data in .jsonl or .log files 
    - log_info() : logs info (message : str) in .jsonl or .log files
"""

# still need to work on the docstring

__version__ = "1.0.0"
__author__ = "MrCode200"

from .retry_decorator import retry
from .run_time_decorator import get_time
from .log_decorator import LoggerManager

__all__ = ["retry", "get_time", LoggerManager]
