from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from calculator import add, divide, multiply, subtract


def test_add_basic():
    assert add(2, 3) == 5


def test_subtract_basic():
    assert subtract(7, 4) == 3


def test_multiply_basic():
    assert multiply(3, 5) == 15


def test_divide_returns_float():
    assert divide(7, 2) == 3.5


def test_divide_by_zero_raises():
    with pytest.raises(ValueError):
        divide(1, 0)
