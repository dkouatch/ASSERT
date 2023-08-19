import pytest

from src.lib.utils.time import *


@pytest.mark.parametrize("year, result", [(2000, True), (1900, False),
                                          (2003, False), (2004, True),
                                          (0, False), (-1, False)])
def test_is_leap_year(year: int, result: bool):
    try:
        findings = is_leap_year(year)
    except:
        assert year < 1
    else:
        assert findings == result


@pytest.mark.parametrize("yyyy, mm, dd, day_of_year",
                         [(0, 0, 0, 0), (1998, 1, 1, 1),
                          (1999, 2, 1, 32), (2000, 3, 1, 61),
                          (2001, 3, 1, 60), (2003, 12, 31, 365),
                          (2004, 12, 31, 366), (2023, 13, 1, 366),
                          (2023, 1, 35, 35), (2023, -1, 31, -1),
                          (2023, 1, -1, -1)])
def test_get_day_of_year(yyyy: int, mm: int, dd: int, day_of_year: int):
    try:
        result = get_day_of_year(yyyy, mm, dd)
    except:
        ref = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        try:
            findings = is_leap_year(yyyy)
        except:
            assert yyyy < 1
        else:
            if findings:
                ref[1] = 29
            assert mm < 1 or mm > 12 or dd < 1 or dd > ref[mm - 1]
    else:
        assert result == day_of_year
