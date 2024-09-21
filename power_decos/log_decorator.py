"""
A logging management module that defines the following class:

- `LoggerManager`: Handles all logging functionality with configurable settings and utility methods.

Classes
=======

- `LoggerManager`: Manages the logging system with configurable settings, including terminal and file logging,
  JSON or text formatting, and rotating log files.

How To Use This Module
======================

1. Import it: ``import logging_manager`` or ``from logging_manager import LoggerManager``.

2. Create an instance of `LoggerManager`:

       logger = LoggerManager()

3. Initialize the logger, specifying options such as logging to terminal, file, and format (JSON or text):

       logger.init_logger(log_in_terminal=True, log_in_file=True)

4. Log messages at various levels (INFO, DEBUG, etc.):

       logger.log_info("This is an informational message")

5. Use `log_func` as a decorator to automatically log function entry, exit, and exceptions:

       @logger.log_func
       def my_function():
           # function code

6. Customize the logging configuration by adding/removing handlers or adjusting log format as needed.

7. Clean up resources explicitly if needed using the `__del__` method which is automatically called when the instance is about to be destroyed.
    This should be used when needing to access the log json files or

    logger.init_logger(log_in_terminal = False) # this will also make you able to access the log files

"""

import os
import platformdirs
import logging
import logging.handlers
from datetime import datetime
from functools import wraps
import inspect

from ._logging_fomatter_json import JSONLineFormatter


class LoggerManager:
    def __init__(self):
        self.logger = logging.getLogger(str(self))
        self.logger.setLevel(logging.DEBUG)

    def init_logger(
            self,
            log_in_terminal: bool = False,
            log_in_file: bool = True,
            logfile_name: str = None,
            log_file_in_json: bool = True,
            use_rotating_file_handler: bool = False,
            max_bytes: int = 1024 * 1024,
            backup_counts: int = 3,
            custom_logfile_formatter=None,
            log_dir_path=None,
            auto_dir_path_arguments=None
    ):
        """
        Initializes the logging system by setting up handlers for logging to the terminal
        and/or a file. Supports JSON and text log formats, as well as rotating file handlers.

        Note: The log file (e.g., .jsonl) cannot be accessed or modified while a handler is actively using it.
        Ensure to release file handlers before accessing the log file.
        This can be done in two ways:

        1. del instance
        2. instance(log_in_file = False)


        :keyword log_in_terminal: If True, logs messages to the terminal.
        :keyword log_in_file: If True, logs messages to a file.
        :keyword logfile_name: The name of the log file. If None, defaults to a name based on the current date.
        :keyword log_file_in_json: If True, formats log messages as JSON lines in the log file.
        :keyword use_rotating_file_handler: If True, uses a rotating file handler.
        :keyword max_bytes: The maximum size (in bytes) of the log file before it is rotated.
        :keyword backup_counts: The number of backup files to keep before deleting the oldest.
        :keyword custom_logfile_formatter: A custom formatter for the log file. Defaults to JSONLineFormatter or a text formatter.
        :keyword logdir_location: The name of the log dir. If left None creates a dir under the \\Users\\<username>\\AppData\\Local\\Logs
        :keyword auto_dir_path_arguments: LoggerManager uses `platformdirs.user_log_path()` to determine the log directory automatically. Provide a dictionary with keys corresponding to the arguments accepted by `platformdirs.user_log_path()`. The dictionary must include all required arguments.
        """
        # check if arguments are not the predefined arguments
        if not use_rotating_file_handler and max_bytes != 1024 * 1024 or backup_counts != 3:
            raise ValueError("If use_rotating_file_handler is false, max_bytes or backup_counts cannot be defined")
        if log_dir_path is not None and auto_dir_path_arguments is not None:
            raise ValueError("auto_dir_path_arguments cant be given if a log_dir_path is given")

        if auto_dir_path_arguments is None:
            auto_dir_path_arguments = {
                "appname": None,
                "appauthor": None,
                "version": None,
                "opinion": True,
                "ensure_exists": False}

        self.logger.handlers.clear()
        logfile_path = self._get_logfile_path(log_dir_path, logfile_name, auto_dir_path_arguments)

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

    def _get_logfile_path(self, log_dir_path: str, logfile_name: str, auto_dir_path_args: dict[str, str | bool]) -> str:
        """
        Constructs the path for the log file and ensures the directory exists.
        If the directory does not exist, create a new one.

        :param log_dir_path: The name of the log dir. If left None creates a dir under the \\Users\\<username>\\AppData\\Local\\Logs
        :param logfile_name: The name of the log file. If left empty creates a file with the date of today.
        :param auto_dir_path_arguments: LoggerManager uses `platformdirs.user_log_path()` to determine the log directory automatically. Provide a dictionary with keys corresponding to the arguments accepted by `platformdirs.user_log_path()`. The dictionary must include all required arguments.
        :return: The full path to the log file.
        """
        if log_dir_path is None:
            caller_script_path = platformdirs.user_log_path(auto_dir_path_args["appname"],
                                                            auto_dir_path_args["appauthor"],
                                                            auto_dir_path_args["version"],
                                                            auto_dir_path_args["opinion"],
                                                            auto_dir_path_args["ensure_exists"])
            log_dir_path = os.path.join(caller_script_path, "logs")

        os.makedirs(log_dir_path, exist_ok=True)

        if logfile_name is None:
            today = datetime.now()
            logfile_name = f"log_{today.month:02d}-{today.day:02d}-{today.year}"

        return os.path.join(log_dir_path, f"{logfile_name}.jsonl")

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
        if use_rotating_file_handler:
            file_handler = file_handler_class(
                filename=logfile_path,
                backupCount=backup_counts,
                maxBytes=max_bytes
            )
        else:
            file_handler = file_handler_class(filename=logfile_path)

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            custom_logfile_formatter
            if custom_logfile_formatter is not None
            else JSONLineFormatter() if log_file_in_json
            else logging.Formatter(
                "[%(levelname)s|%(custom_file_name)s/%(custom_func_name)s|%(custom_lineno)s] %(asctime)s - args/kwargs: %(custom_args)s/%(custom_kwargs)s Returned: %(message)s"
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
                "[%(levelname)s|%(custom_file_name)s/%(custom_func_name)s|%(custom_lineno)s] %(asctime)s - args/kwargs: %(custom_args)s/%(custom_kwargs)s Returned: %(message)s"
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
        extra = {
            "custom_file_name": caller_filename,  # Use default value None if not present
            "custom_lineno": lineno,
            "custom_func_name": None,
            "custom_args": {},
            "custom_kwargs": {},
            "info": log_info,
            "exc": None
        }

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
                    "custom_file_name": caller_filename,
                    "custom_lineno": lineno,
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

    def __del__(self):
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
