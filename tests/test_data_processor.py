import pytest
from src.data_processor import process_data, filter_data

def test_process_data():
    assert process_data([1, 2, 3]) == [2, 4, 6]
    assert process_data("string") == [2, 4, 6]  # This test will fail

def test_filter_data():
    assert filter_data([1, 2, 3, 4, 5], 3) == [4, 5]
    assert filter_data([1, 2, 3, 4, 5], 6) == []  # This test will fail