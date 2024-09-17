"""
Module containing the retry decorator

**Decorators**:
    - **retry**: Reexecutes function on Exception.
"""

from time import sleep
from functools import wraps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry(
    retries: int = 3,
    delay: float = 1,
    raise_exception: bool = False,
    exception_types: BaseException | tuple[BaseException] = Exception
) -> callable:
    """
    Reexecutes a function upon encountering an exception.

    :keyword int retries: Number of times the function should retry upon encountering an exception.
    :keyword float delay: Time in seconds to wait between retry attempts.
    :keyword bool raise_exception: Whether to raise the exception after exhausting all retries.
    :keyword exception_types: Exception types that should trigger a retry. Can be a single type or a tuple of types.

    :raises ValueError: If `retries` is less than 1 or `delay` is less than or equal to 0.
    :raises TypeError: If `exception_types` is not a type or a tuple of types.
    """
    if retries < 1 or delay <= 0:
        raise ValueError("Arguments are wrong! retries >= 1; delay > 0")

    if isinstance(raise_exception, (type, tuple)):
        raise TypeError("Exception(s) passed is not a type or a tuple of types.")

    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> any:
            for attempt in range(1, retries + 1):
                try:
                    logger.info(f"Attempt {attempt}/{retries} for function '{func.__name__}'")
                    return func(*args, **kwargs)

                except exception_types as exc:
                    if attempt == retries:
                        print(f"Function '{func.__name__}' failed after {retries} attempts")
                        if raise_exception:
                            raise exc
                        logger.error(f"Error: {exc}")
                    else:
                        logger.warning(f"Retrying after exception: {exc}")
                        sleep(delay)
        return wrapper
    return decorator
