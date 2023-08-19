"""
General utilities for building and testing

      * get_hostname

  - Directories/Files
      * mkdir_p
      * find_files
      * clean_scratch
      * clean_dir
      * copy_file
      * which
      * grep_file
      * sed_inplace
      * create_link

  - Repository
      * get_repotype


"""
import datetime


def is_leap_year(year: int) -> bool:
    """
    Determine if a year is a leap year or not.
    Criteria:
        - Year must be divisible by 4
        - If it is an 'end of the century' year (a.k.a. divisible by 100)
          then it must be divisible by 400

    Parameters
    ---------
    year : int
        The year as four digits

    Returns
    -------
    bool
        True (for leap year) or False.

    """
    if year < 1:
        raise Exception('Least year is 1 A.D.')
    else:
        return year % 400 == 0 or (year % 4 == 0 and year % 100 != 0)


def get_day_of_year(yyyy: int, mm: int, dd: int) -> int:
    """
    Determine the number of days since January 1st.

    Parameters
    ---------
    yyyy : int
        The year as four digits
    mm : int
        The month as two digits
    dd : int
        The day as two digits

    Returns
    -------
    int
        The number of days since January 1st.
    """
    days_per_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if is_leap_year(yyyy):
        days_per_month[1] = 29

    if (mm < 1 or mm > 12 or
            dd < 1 or dd > days_per_month[mm - 1]):
        raise Exception('Enter valid month (01-12) and appropriate day')

    return sum(days_per_month[0:(mm - 1)]) + dd


def set_datetime_stamp():
    return datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
