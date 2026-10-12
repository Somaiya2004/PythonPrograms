import importlib

module = importlib.import_module("codes.prime_number")


def test_is_0_is_prime():
    assert module.is_prime(0) is False


def test_is_5_is_prime():
    assert module.is_prime(5) is True

# python -m pytest .\test_case\test_prime_number.py