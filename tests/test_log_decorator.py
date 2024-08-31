import pytest
from power_decos import log_decorator
import json
import shutil, os


@log_decorator.log_func()
def func_log():
    return "hello"


@log_decorator.log_func()
def func_log_with_exc():
    with pytest.raises(Exception):
        raise Exception("This is a test for the @log decorator")


def test_func_log(stdout):
    func_log()

    capture = stdout.readout()
    print(capture)
    assert capture == "l"


def test_files_created():
    # Open the file in read mode
    with open("tests/logs/log.jsonl", "r") as file:
        # Initialize a list to hold the JSON objects
        data = []
        
        # Read each line in the file
        for line in file:
            try:
                # Parse the JSON object from the line and append to the list
                json_object = json.loads(line.strip())
                data.append(json_object)
            except json.JSONDecodeError as e:
                # Print an error message if a line cannot be parsed
                print(f"Error decoding JSON line: {e}")

    # Print the collected data
    print(data)


log_decorator.init_logger(True, True, None, True, True)

test_func_log()
#test_files_created()
