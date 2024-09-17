"""
Module: logging_manager
=======================

This module handles all logging functionality through the `LoggerManager` class.

Classes:
--------

- **LoggerManager**: Manages the logging system with various utility methods.
  - **__init__()**: Initializes the `LoggerManager` instance.
  - **init_logger()**: Configures logging system settings.
  - **_get_logfile_path()**: Constructs the path for the log file and ensures the directory exists.
  - **_add_file_handler()**: Adds a file handler to the logger with specified configurations.
  - **_add_stream_handler()**: Adds a stream handler to the logger.
  - **_get_lineNo_fileName()**: Retrieves the line number and file name of the caller.
  - **log_info()**: Logs informational messages.
  - **log_func()**: Decorator to log function executions and exceptions.
"""

import os
import sys
import logging
import logging.handlers
from datetime import datetime
from functools import wraps
import inspect

from .logging_fomatter_json import JSONLineFormatter


class LoggerManager:
    def __init__(self):
        self.logger = logging.getLogger(str(self))
        self.logger.setLevel(logging.DEBUG)

    def init_logger(
        self,
        log_in_terminal: bool = False,
        log_in_file: bool = False,
        logfile_name: str = None,
        log_file_in_json: bool = True,
        use_rotating_file_handler: bool = False,
        max_bytes: int = 1024 * 1024,
        backup_counts: int = 3,
        custom_logfile_formatter = None,
    ):
        """
        Initializes the logging system by setting up handlers for logging to the terminal
        and/or a file. Supports JSON and text log formats, as well as rotating file handlers.

        :keyword log_in_terminal: If True, logs messages to the terminal.
        :keyword log_in_file: If True, logs messages to a file.
        :keyword logfile_name: The name of the log file. If None, defaults to a name based on the current date.
        :keyword log_file_in_json: If True, formats log messages as JSON lines in the log file.
        :keyword use_rotating_file_handler: If True, uses a rotating file handler.
        :keyword max_bytes: The maximum size (in bytes) of the log file before it is rotated.
        :keyword backup_counts: The number of backup files to keep before deleting the oldest.
        :keyword custom_logfile_formatter: A custom formatter for the log file. Defaults to JSONLineFormatter or a text formatter.
        """
        self.logger.handlers.clear()
        logfile_path = self._get_logfile_path(logfile_name)

        if log_in_file:
            self._add_file_handler(
                logfile_path,
                log_file_in_json,
                use_rotating_file_handler,
                max_bytes,
                backup_counts,
                custom_logfile_formatter
            )

        if log_in_terminal:
            self._add_stream_handler(custom_logfile_formatter)

    def _get_logfile_path(self, logfile_name: str) -> str:
        """
        Constructs the path for the log file and ensures the directory exists.
        If the directory does not exist, create a new one.

        :param logfile_name: The name of the log file. If left empty creates a file with the date of today.
        :return: The full path to the log file.
        """
        script_path = os.path.abspath(sys.argv[0])
        script_dir = os.path.dirname(script_path)
        log_dir = os.path.join(script_dir, "logs")
        os.makedirs(log_dir, exist_ok=True)

        if logfile_name is None:
            today = datetime.now()
            logfile_name = f"log_{today.month:02d}-{today.day:02d}-{today.year}"

        return os.path.join(log_dir, f"{logfile_name}.jsonl")

    def _add_file_handler(
        self,
        logfile_path: str,
        log_file_in_json: bool,
        use_rotating_file_handler: bool,
        max_bytes: int,
        backup_counts: int,
        custom_logfile_formatter=None
    ):
        """
        Adds a file handler to the logger with specified configurations.

        :param logfile_path: The path to the log file.
        :param log_file_in_json: If True, uses JSON format for the log file.
        :param use_rotating_file_handler: If True, uses a rotating file handler.
        :param max_bytes: The maximum size of the log file before rotation.
        :param backup_counts: The number of backup files to keep.
        :keyword custom_logfile_formatter: A custom formatter for the log file.
            DEFAULT: uses in built formatter
        """
        file_handler_class = logging.handlers.RotatingFileHandler if use_rotating_file_handler else logging.FileHandler
        file_handler = file_handler_class(
            filename=logfile_path,
            maxBytes=max_bytes,
            backupCount=backup_counts
        )

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            custom_logfile_formatter
            if custom_logfile_formatter is not None
            else JSONLineFormatter() if log_file_in_json
            else logging.Formatter(
                "[%(levelname)s|%(fileName)s/%(custom_func_name)s|%(lineNo)s] %(asctime)s - args/kwargs: %(custom_args)s/%(custom_kwargs)s Returned: %(message)s"
            )
        )
        self.logger.addHandler(file_handler)

    def _add_stream_handler(self, custom_logfile_formatter=None):
        """
        Adds a stream handler to the logger.

        :keyword custom_logfile_formatter: A custom formatter for the terminal logs.
        """
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.DEBUG)
        stream_handler.setFormatter(
            custom_logfile_formatter
            if custom_logfile_formatter is not None
            else logging.Formatter(
                "[%(levelname)s|%(fileName)s/%(custom_func_name)s|%(lineNo)s] %(asctime)s - args/kwargs: %(custom_args)s/%(custom_kwargs)s Returned: %(message)s"
            )
        )
        self.logger.addHandler(stream_handler)

    def _get_lineNo_fileName(self) -> tuple[str, str]:
        """
        Retrieves the line number and file name of the caller.

        :return: A tuple containing the file name and line number of the caller.
        """
        caller_frame = inspect.currentframe().f_back
        caller_filename = os.path.basename(caller_frame.f_globals["__file__"])
        lineno = caller_frame.f_lineno
        return caller_filename, lineno

    def log_info(self, log_info: str):
        """
        Logs informational messages to the terminal or log file.

        :param log_info: The message to be logged.
        """
        caller_filename, lineno = self._get_lineNo_fileName()
        extra = {"fileName": caller_filename, "lineNo": lineno, "log_info": log_info}
        self.logger.info("NonFunctionLog", extra=extra)

    def log_func(self, skip_exception: bool = False, log_info: str = None) -> callable:
        """
        Decorator to log function executions and exceptions.

        :keyword skip_exception: If True, exceptions are logged but not raised. `DEFAULT: False`
        :keyword log_info: Additional information to log. `DEFAULT: Doesn't log extra information`
        :return: The decorated function.
        """
        def decorator(func: callable) -> callable:
            @wraps(func)
            def wrapper(*args, **kwargs) -> any:
                caller_filename, lineno = self._get_lineNo_fileName()
                extra = {
                    "fileName": caller_filename,
                    "lineNo": lineno,
                    "custom_func_name": func.__name__,
                    "custom_args": args,
                    "custom_kwargs": kwargs,
                    "info": log_info,
                }
                if log_info is not None:
                    extra["info"] = log_info

                try:
                    result: any = func(*args, **kwargs)
                    self.logger.debug(result, extra=extra)
                    return result

                except Exception as exc:

                    extra["exc"] = exc
                    self.logger.exception(exc.__class__, extra=extra)

                    if not skip_exception:
                        raise exc

            return wrapper

        return decorator
