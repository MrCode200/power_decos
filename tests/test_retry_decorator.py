"""
test_retry_raise_exception_assertion not working
"""

from power_decos import retry
import time
import pytest


def test_retry_4_times():
    tries = 0

    @retry(retries=4, delay=1.1, raise_exception=False)
    def always_fail():
        nonlocal tries
        tries += 1
        raise Exception("This is a test for the @retry decorator")

    always_fail()  # Call the function
    assert tries == 4  # Ensure it was retried 4 times


def test_retry_raise_exception_assertion():
    @retry(retries=4, delay=1.1, raise_exception=True)
    def always_fail():
        raise Exception("This is a test for the @retry decorator")

    with pytest.raises(Exception) as excinfo:
        always_fail()  # Expect this to raise an exception

    # Verify the exception message if needed
    assert str(excinfo.value) == "This is a test for the @retry decorator"


def test_retry_delay():
    delay = 1.1
    tries = 4

    @retry(retries=tries, delay=delay, raise_exception=False)
    def always_fail():
        raise Exception("This is a test for the @retry decorator")

    start_time = time.time()
    always_fail()
    end_time = time.time()

    elapsed_time = end_time - start_time

    expected_delay = delay * (tries - 1)  # 1.1 seconds delay * (4 retries - 1)
    assert True if expected_delay <= elapsed_time < expected_delay + 1 else False, f"Delay did not work as expected. Elapsed time: {elapsed_time}. Excpected delay: {expected_delay}"


if __name__ == "__main__":
    pytest.main()
