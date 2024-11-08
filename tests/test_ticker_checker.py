import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from MadMoney.validation import is_valid_ticker


def test_ticker_checker():
    assert is_valid_ticker("AAPL") == True
    assert is_valid_ticker("TSLA") == True
    assert is_valid_ticker("AMZN") == True
    assert is_valid_ticker("MSFT") == True
    assert is_valid_ticker("GOOGL") == True
    assert is_valid_ticker("FB") == True
    assert is_valid_ticker("NFLX") == True
    assert is_valid_ticker("NVDA") == True

    assert is_valid_ticker("INVALIDTICKER123") == False
    assert is_valid_ticker("ZZZZZ") == False
    assert is_valid_ticker("1234") == False
    assert is_valid_ticker("ABCXYZ") == False
    assert is_valid_ticker("QWERTY") == False
    assert is_valid_ticker("NOEXIST") == False
    assert is_valid_ticker("XYZ123") == False
