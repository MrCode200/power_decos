import logging

from power_decos import get_time
import pytest

def test_decorator_logs_execution_time(caplog):
    @get_time
    def sample_function():
        return "test"

    with caplog.at_level(logging.INFO):
        result = sample_function()

    assert result == "test"
    assert "Function sample_function took" in caplog.text
