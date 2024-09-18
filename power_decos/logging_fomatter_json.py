"""
Module containing premade JSONLineFormatter for the logging pckg

JSONLineFormatter [class]
- format -> str : gets all data logged, change format acceptable for jsonl and turns it into string
"""

import logging
import json
from datetime import datetime


class JSONLineFormatter(logging.Formatter):
    """
    Formatter for logging package used in power_decos package.
    Converts the log record into a JSON-formatted string suitable for JSONL.
    """

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record into a JSON string.

        :param record: The log record that needs to be formatted.
        :return: A JSON string representing the log entry.
        """
        # Prepare log entry dictionary
        log_entry = {
            "timestamp": str(datetime.now()),  # Use ISO format for timestamp
            "level": record.levelname,
            "file_name": getattr(record, "custom_file_name"),  # Use default value None if not present
            "lineno": getattr(record, "custom_lineno"),
            "function_name": getattr(record, "custom_func_name"),
            "returned": record.getMessage(),  # This gets the actual log message
            "args": getattr(record, "custom_args"),
            "kwargs": getattr(record, "custom_kwargs"),
            "info": getattr(record, "info"),
            "exc": self.formatException(record.exc_info) if record.exc_info else None
        }

        # Convert the log entry to a JSON string
        return json.dumps(log_entry)
