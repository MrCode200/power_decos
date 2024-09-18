"""
test_func_log_terminal not working
"""
import json
import os
import shutil
import time

import pytest
import logging
from datetime import datetime
from power_decos import LoggerManager
from unittest.mock import patch, mock_open

# Create an instance of LoggerManager
logger_manager = LoggerManager()

@pytest.fixture(scope="session", autouse=True)
def cleanup_files():
    yield

    def cleanup():
        directory_to_cleanup = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        if os.path.exists(directory_to_cleanup):
            shutil.rmtree(directory_to_cleanup)

    cleanup()

def test_get_logfile_path_creates_directory():
    """
    Test function to validate the creation of log directory and file path by the LoggerManager's _get_logfile_path method.
    Also validates the correct date-based naming of the log file when logfile_name is None.
    """
    logger_manager.init_logger(log_in_terminal=True, log_in_file=True)

    today = datetime.now()
    expected_logfile_name = f"log_{today.month:02d}-{today.day:02d}-{today.year}"

    # Expected log directory and file path
    expected_log_dir_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
    expected_path = os.path.join(expected_log_dir_path, f"{expected_logfile_name}.jsonl")

    # Validate if the directory and file path exist
    assert os.path.exists(expected_log_dir_path), f"Log directory not created at expected path: {expected_log_dir_path}"
    assert os.path.exists(expected_path), f"Log file not created at expected path: {expected_path}"


def test_func_log_terminal(caplog):
    """
    Test to check if the terminal log is working correctly using caplog.
    """
    # Reinitialize logger to only log in the terminal
    logger_manager.init_logger(log_in_terminal=True, log_in_file=False)

    with caplog.at_level(logging.INFO):
        logger_manager.log_info("Testing terminal log")

    # Check if logs were captured in the terminal
    assert len(caplog.records) == 1, "No logs captured in terminal"
    log_record = caplog.records[0]

    # Validate the log record contents
    assert log_record.message == "NonFunctionLog", "Unexpected log message"
    assert log_record.levelname == "INFO", "Unexpected log level"
    
    
def test_func_log_file_json():
    """
    Test to check if the json log is working correctly.
    """
    # Reinitialize logger to only log in the terminal
    logger_manager.init_logger(log_in_terminal=False, log_in_file=True, log_file_in_json=True, logfile_name="test_log")
    # Excpected Log json file
    expected_log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs\\test_log.jsonl")

    # Define a function to log
    @logger_manager.log_func()
    def important_func(x: int, y: int):
        return x + y

    # Call the function to generate logs
    important_func(1, 2)

    # Give some time for the log file to be written (if necessary)
    import time
    # free process to be able to access the file via cleanup()
    logger_manager.init_logger(False, False)
    time.sleep(1)

    # Check if the log file exists
    assert os.path.exists(expected_log_file_path), f"Log file not found at expected path: {expected_log_file_path}"

    # Read the JSONL log file and validate contents
    with open(expected_log_file_path, "r") as json_log_file:
        for line in json_log_file:
            try:
                log_entry = json.loads(line)
            except json.JSONDecodeError:
                pytest.fail(f"Log file at {expected_log_file_path} contains invalid JSON")

            # Validate the log entry structure
            assert "timestamp" in log_entry, "Missing 'timestamp' field in log entry"
            assert "level" in log_entry, "Missing 'level' field in log entry"
            assert "file_name" in log_entry, "Missing 'file_name' field in log entry"
            assert "lineno" in log_entry, "Missing 'lineno' field in log entry"
            assert "function_name" in log_entry, "Missing 'function_name' field in log entry"
            assert "returned" in log_entry, "Missing 'returned' field in log entry"
            assert "exc" in log_entry, "Log entry missing 'exc' field"

            # Further checks based on expected values
            assert log_entry["level"] == "DEBUG", f"Unexpected log level in entry: {log_entry}"
            assert log_entry["file_name"] == "log_decorator.py", f"Unexpected file name in entry: {log_entry}"
            assert log_entry["function_name"] == "important_func", f"Unexpected function name in entry: {log_entry}"
            assert log_entry["returned"] == "3", f"Unexpected returned value: {log_entry['returned']}"
            assert log_entry["args"] == [1, 2], f"Unexpected args: {log_entry['args']}"
            assert log_entry["kwargs"] == {}, f"Unexpected kwargs: {log_entry['kwargs']}"

            try:
                datetime.fromisoformat(log_entry["timestamp"].replace("Z", "+00:00"))
            except ValueError:
                pytest.fail(f"Unexpected timestamp format in entry: {log_entry['timestamp']}")


if __name__ == "__main__":
    pytest.main()
