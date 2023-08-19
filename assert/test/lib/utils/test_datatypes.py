import pytest

from src.lib.utils.datatypes import *


@pytest.mark.parametrize("string, result",
                         [('YES', True), ('YEs', True), ('YeS', True),
                          ('Yes', True), ('yES', True), ('yEs', True),
                          ('yeS', True), ('yes', True), ('Y', True),
                          ('y', True), ('NO', False), ('No', False),
                          ('nO', False), ('no', False), ('N', False),
                          ('n', False), ('maybe', True)])
def test_true_or_false(string: str, result: bool):
    if string == 'maybe':
        try:
            true_or_false(string)
        except:
            assert True
        else:
            assert False
    else:
        assert true_or_false(string) == result


@pytest.mark.parametrize("string, result",
                         [('1.0', True), ('5.7', True), ('-74.3', True),
                          ('D', False), ('4/5', False), ('35.4 * 2', False),
                          ('0', False), ('0.0', True)])
def test_is_string_float(string: str, result: bool):
    assert is_string_float(string) == result


@pytest.mark.parametrize("string, result",
                         [('1.0', False), ('-3', True), ('578', True),
                          ('D', False), ('4/5', False), ('-9.9', False),
                          ('0', True), ('0.0', False)])
def test_is_string_int(string: str, result: bool):
    assert is_string_int(string) == result
