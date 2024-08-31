import pytest

from decorators import retry

tries = 0


@retry(retries=4, delay=1.1, raise_exception=False)
def test_retry_skip_exception():
    tries += 1
    raise Exception("This is a test for the @retry decorator")

    assert tries == 4

tries = 0




@retry(retries=4, delay=1.1, raise_exception=True)
def test_retry_raise_exception():
    tries += 1
    if tries == 4:
        with pytest.raises(Exception):
            print(1)
    else:
        raise Exception("This is a test for the @retry decorator")
