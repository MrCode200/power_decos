"""
Module containin handling all logging code

- log_init() : init and changes how data should be logged
- log_func() : logs exc data in .jsonl or .log files 
- log_info() : logs info (message : str) in .jsonl or .log files
"""

import os
import sys
from datetime import datetime
import inspect

import logging
import logging.handlers
from functools import wraps

from .logging_fomatter_json import JSONLineFormatter


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def init_logger(
    log_in_terminal: bool = False,
    log_in_file: bool = False,
    logfile_name: str = None,
    log_file_in_json: bool = True,
    use_rotating_file_handler: bool = False,
    max_bytes: int = 1024 * 1024,
    backup_counts: int = 3,
    custom_logfile_formatter=None,
):
    """
    Initializes the logging system by setting up handlers for logging to the terminal
    and/or a file. Supports JSON and text log formats, as well as rotating file handlers.

    Args:
        log_in_terminal (bool): If True, logs messages to the terminal.
        log_in_file (bool): If True, logs messages to a file.
        logfile_name (str, optional): The name of the log file. If None, defaults to a name 
                                       based on the current date.
        log_file_in_json (bool): If True, formats log messages as JSON lines in the log file.
        use_rotating_file_handler (bool): If True, uses a rotating file handler that 
                                          creates a new file when the log file size exceeds 
                                          `max_bytes`.
        max_bytes (int): The maximum size (in bytes) of the log file before it is rotated.
        backup_counts (int): The number of backup files to keep before deleting the oldest.
        custom_logfile_formatter (logging.Formatter, optional): A custom formatter for the log file. 
                                                               If None, defaults to JSONLineFormatter 
                                                               or a text formatter depending on 
                                                               `log_file_in_json`.

    """

    logger.handlers.clear()

    # get path of script which called init_logger
    script_path = os.path.abspath(sys.argv[0])
    script_dir = os.path.dirname(script_path)
    # create logs directory if it doesnt exist
    log_dir = os.path.join(script_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    if logfile_name is None:
        today = datetime.now()
        logfile_name = f"log_{today.month:02d}-{today.day:02d}-{today.year}"
    logfile_path = os.path.join(log_dir, f"{logfile_name}.jsonl")

    if log_in_file:
        # create and add FileHandler or RotatingFileHandler
        if use_rotating_file_handler:
            file_handler = logging.handlers.RotatingFileHandler(
                filename=logfile_path, maxBytes=max_bytes, backupCount=backup_counts
            )
        else:
            file_handler = logging.FileHandler(logfile_path)

        file_handler.setLevel(logging.DEBUG)

        if log_file_in_json:
            file_handler.setFormatter(
                custom_logfile_formatter
                if custom_logfile_formatter is not None
                else JSONLineFormatter
            )
        else:
            file_handler.setFormatter(
                logging.Formatter(
                    custom_logfile_formatter
                    if custom_logfile_formatter is not None
                    else "[%(levelname)s|%(fileName)s/%(custom_func_name)s|%(lineNo)s] %(asctime)s -args/kwargs: %(custom_args)s/%(custom_kwargs)s Returned: %(message)s"
                )
            )

        logger.addHandler(file_handler)

    if log_in_terminal:  # doesnt work
        # create and add StreamHandler
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(
            logging.Formatter(
                custom_logfile_formatter
                if custom_logfile_formatter is not None
                else "[%(levelname)s|%(fileName)s/%(custom_func_name)s|%(lineNo)s] %(asctime)s -args/kwargs: %(custom_args)s/%(custom_kwargs)s Returned: %(message)s"
            )
        )

        logger.addHandler(stream_handler)


def get_lineNo_fileName() -> tuple[str, str]:
    # get lineno and caller func.__name__
    caller_frame = inspect.currentframe().f_back
    caller_filename = caller_frame.f_globals["__file__"]
    caller_filename = os.path.basename(caller_filename)
    lineno = caller_frame.f_lineno

    return caller_filename, lineno


def log_info(log_info: str):
    """
    Function to log info in terminal or logfile

    **Params:**
    - log_info: str -> info which gets logged
    """

    caller_filename, lineno = get_lineNo_fileName()

    extra = {"fileName": caller_filename, "lineNo": lineno, "log_info": log_info}
    logger.info("NonFunctionLog", extra=extra)


def log_func(
    skip_exception: bool = False,
    log_info: str = None,
) -> callable:
    """
    Decorator to log executions in terminal or logfile

    **Params:**
    - skip_exception: bool -> to skip exception or stop program on exception
    - log_info: str -> info which gets logged extra
    """
    caller_filename, lineno = get_lineNo_fileName()

    def decorator(func: callable) -> callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> any:
            extra = {
                "fileName": caller_filename,
                "lineNo": lineno,
                "custom_func_name": func.__name__,
                "custom_args": args,
                "custom_kwargs": kwargs,
            }
            if log_info is not None:
                extra["info"] = log_info
            try:
                result: any = func(*args, **kwargs)

                logger.debug(result, extra=extra)

                return result
            except Exception as exc:
                extra["exc"] = exc
                logger.exception(exc.__class__, extra=extra)
                if not skip_exception:
                    raise exc

        return wrapper

    return decorator
