"""
test_func_log_terminal not working
"""

import json
from datetime import datetime
import os, sys
import logging

from power_decos import LoggerManager

import pytest


def test_get_logfile_path_creates_directory():
    """_get_logfile_path creates the log directory if it doesn't exist"""
    logger_manager = LoggerManager()
    logfile_path = logger_manager.init_logger()

    today = datetime.now()
    excpected_logfile_name = f"log_{today.month:02d}-{today.day:02d}-{today.year}"

    log_dir = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "logs")
    expected_path = os.path.join(log_dir, f"{excpected_logfile_name}.jsonl")
    assert os.path.exists(log_dir)
    assert logfile_path == expected_path


if __name__ == "__main__":
    pytest.main()
