import pytest
from power_decos import log_decorator
import json
import shutil, os

log_decorator.init_logger(True, True, "log", True, True)


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
    assert capture == "l"


def test_files_created():
    # doesnt work

    with open("logs/log.jsonl", "r") as file:
        data = json.load(file)

    print(data[0])


# test_files_created()
func_log()
