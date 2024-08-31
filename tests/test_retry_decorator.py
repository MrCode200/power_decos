"""
test_retry_raise_exception_assertion not working
"""

import pytest
from power_decos import retry

# Global variable for counting retries
tries = 0

@retry(retries=4, delay=1.1, raise_exception=False)
def test_retry_skip_exception():
    global tries
    tries += 1
    raise Exception("This is a test for the @retry decorator")

def test_retry_skip_exception_assertion():
    global tries
    tries = 0  # Reset `tries` before running the test
    test_retry_skip_exception()  # Call the function
    assert tries == 4  # Ensure it was retried 4 times

# Reset `tries` for the next test
tries = 0

@retry(retries=4, delay=1.1, raise_exception=True)
def test_retry_raise_exception():
    global tries
    tries += 1
    if tries < 4:
        raise Exception("This is a test for the @retry decorator")
    return "completed"

def test_retry_raise_exception_assertion():
    global tries
    tries = 0  # Reset `tries` before running the test
    with pytest.raises(Exception) as excinfo:
        test_retry_raise_exception()  # Expect this to raise an exception
    
    # Verify the exception message if needed
    assert str(excinfo.value) == "This is a test for the @retry decorator"
    
    # Ensure it was retried the correct number of times
    assert tries == 4

if __name__ == "__main__":
    import pytest
    pytest.main()