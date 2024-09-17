"""
Package full of utility decorators

**Decorators**:

- `retry(num_of_retries=3, interval=1)`: Retries a function upon failure for a specified number of times, with a delay between attempts.

- `get_time()`: Measures and prints the execution time of the decorated function.

- `log_decorator`:
    - `log_init()`: Initializes and configures how logging data should be handled (e.g., terminal, file, JSON).
    - `log_func()`: Logs the entry, exit, and any exceptions of a function to `.jsonl` or `.log` files.
    - `log_info(message: str)`: Logs custom informational messages to `.jsonl` or `.log` files.

Module provides easy-to-use decorators for common tasks like retrying failed operations, measuring execution time, and structured logging.

**Params**:
- __version__
- __author__
"""

# still need to work on the docstring

__version__ = "1.0.0"
__author__ = "MrCode200"

from .retry_decorator import retry
from .run_time_decorator import get_time
from .log_decorator import LoggerManager

__all__ = ["retry", "get_time", LoggerManager]
