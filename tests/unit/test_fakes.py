import pytest

from quickanalysis.analysis.fakes import emptylist

def test_emptylist():
    assert emptylist() == []