"""
test_func_log_terminal not working
"""

from unittest.mock import patch
import json
from datetime import datetime
import os

from power_decos import log_decorator

@log_decorator.log_func()
def func_log():
    return "hello"

def test_func_log_terminal(capsys):
    # Call the function
    func_log()

    # Capture the output
    captured = capsys.readouterr()

    # Extract relevant parts of the output
    expectedOutputFront = "[DEBUG|log_decorator.py/func_log|"
    expectedOutputEnd = "-args/kwargs: ()/{} Returned: hello"

    # Ensure the captured output contains expected parts
    assert expectedOutputFront in captured.out
    assert expectedOutputEnd in captured.out

def first_line_of_jsonl():
    today = datetime.now()
    logfile_name = f"log_{today.month:02d}-{today.day:02d}-{today.year}"
    logfile_path = os.path.join("tests\logs", f"{logfile_name}.jsonl")

    # Open the file and read the first line
    with open(logfile_path, "r") as file:
        first_line = file.readline().strip()
    
    return json.loads(first_line)

def test_first_line_data():
    # Get the expected data with a buffer for timestamp
    expected_data = {
        "timestamp": str(datetime.now()),
        "level": "DEBUG",
        "file_name": "log_decorator.py",
        "lineno": 140,
        "function_name": "func_log",
        "returned": "hello",
        "args": [],
        "kwargs": {},
        "info": None,
        "exc": None
    }
    
    # Read the first line of the JSONL file
    actual_data = first_line_of_jsonl()
    
    # Check if the actual data is close to expected data
    assert (
        actual_data["level"] == expected_data["level"] and
        actual_data["file_name"] == expected_data["file_name"] and
        actual_data["lineno"] == expected_data["lineno"] and
        actual_data["function_name"] == expected_data["function_name"] and
        actual_data["returned"] == expected_data["returned"] and
        actual_data["args"] == expected_data["args"] and
        actual_data["kwargs"] == expected_data["kwargs"] and
        actual_data["info"] == expected_data["info"] and
        actual_data["exc"] == expected_data["exc"]
    ), f"Expected {expected_data} but got {actual_data}"

# Initialize logger if necessary (remove if not needed)
# log_decorator.init_logger(True, True, None, True, True)

# Use pytest to run the tests
if __name__ == "__main__":
    import pytest
    pytest.main()
