from unittest.mock import patch
from main import APIFetcher
from main import Main


def test_getTickets():
    main = Main()
    m = main.programManager.callCorrectMethod("1")
    af = APIFetcher()
    len_t = len(af.getTickets())
    assert (len(m) == len_t)
    assert (len_t == 100)


def get_input(text):
    return input(text)


def test_correct_ticket_by_ID():
    main = Main()

    with patch('builtins.input', return_value="3"):
        t = main.programManager.listAllTickets()[2]
        assert (main.programManager.callCorrectMethod("2") == t)


def test_wrong_ticket_by_ID():
    main = Main()

    with patch('builtins.input', return_value="200"):
        ret = "No ticket found by that ID."
        assert (main.programManager.callCorrectMethod("2") == ret)


if __name__ == '__main__':
    import pytest

    pytest.main(['main_tester.py'])
