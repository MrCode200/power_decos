import pytest

def main():
    pytest.main(["-v", "--maxfail=3"])

if __name__ == '__main__':
    main()