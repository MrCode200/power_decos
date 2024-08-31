import pytest
import io

from time import sleep

from power_decos import get_time, init_logger

init_logger(True)

@get_time
def func():
    sleep(1.5)
    
def test_get_time(capfd):
    func()
    capture = capfd.readouterr()
    assert "Function func" in capture.out

if __name__ == "__main__":
    import pytest
    pytest.main()
