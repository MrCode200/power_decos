"""
Module containing the retry decorator

- retry : retries function on exception
"""

from time import sleep
from functools import wraps

def retry(retries: int = 3, delay: float = 1, raise_exception: bool = False) -> callable:
    """
    Reexecutes function on Exception

    *Param:*
        retries: int -> how many times it should retry on exception
        delay: float -> how long it should wait till retriing
        raise_exception: bool -> raise_exception at the end of retries or not
    """

    if retries < 1 or delay <= 0:
        raise ValueError("Argument passed are wrong! retries >= 1;  delay > 0")

    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> any:
            for i in range(retries):

                try:
                    print(f"retrying {func.__name__} (attempt {i}/{retries}) ")
                    return func(*args, **kwargs)
                
                except Exception as exc:
                    if i == retries - 1:
                        
                        print(f"'{func.__name__}()' failed after {retries} tries")
                        if raise_exception:
                            raise exc

                        print(f"Error: {repr(exc)}.")
                    else:
                        sleep(delay)

        return wrapper
    return decorator