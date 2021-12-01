from unittest.mock import patch
from APIFetcher import APIFetcher
from main import calcNextNewLimits, calcPrevNewLimits


# I HAD TESTS FOR THE APIFETCHER BUT REMOVED SINCE IT WOULD NEED CREDENTIALS

def test_calcPrevNewLimits_standard():
    assert calcPrevNewLimits([25, 50]) == [0, 25]


def test_calcPrevNewLimits_non_25():
    assert calcPrevNewLimits([50, 67]) == [25, 50]


def test_calcNextNewLimits_standard():
    assert calcNextNewLimits([25, 50], 100) == [50, 75]


def test_calcNextNewLimits_non_25():
    assert calcNextNewLimits([50, 75], 87) == [75, 86]


if __name__ == '__main__':
    import pytest

    pytest.main(['main_tester.py'])
