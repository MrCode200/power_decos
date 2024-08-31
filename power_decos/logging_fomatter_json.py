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
    Formatter for logging pckg used in power_decos pckg
    """

    def format(record: logging.LogRecord) -> str:
        # Prepare log entry dictionary
        log_entry = {
            "timestamp": str(datetime.now()),  # Use ISO format for timestamp
            "level": record.levelname,
            "file_name": getattr(record, "fileName"),
            "lineno": getattr(record, "lineNo"),
            "function_name": getattr(record, "custom_func_name", None),
            "returned": record.getMessage(),
            "args": getattr(record, "custom_args", {}),
            "kwargs": getattr(record, "custom_kwargs", {}),
            "info": getattr(record, "info", None),
            "exc": getattr(record, "exc", None),
        }

        return json.dumps(log_entry)
