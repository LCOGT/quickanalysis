import pytest

from analysis.fakes import emptylist

def test_emptylist():
    assert emptylist() == []