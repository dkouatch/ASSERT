#!/usr/bin/env python

"""
Utilities for manipulating data types.

    - true_or_false
    - is_string_float
    - is_string_int
    - print_dict
"""

import sys


def true_or_false(a):
    """ 
    Convert yes or no into True or False

    Parameters
    ----------
    a : str
        The variable that can be 'y', 'Y', 'yes',
        'YES', 'Yes', 'n', 'N', 'no', 'No', 'NO'

    Returns
    -------
    bool
        True (for 'yes') or False (for 'no').
    """
    if a.lower().strip() == 'yes' or a.lower().strip() == 'y':
        return True
    elif a.lower().strip() == 'no' or a.lower().strip() == 'n':
        return False
    else:
        raise Exception('Not a valid [y/n] entry')


def is_string_float(string):
    """
    Check if input string is float. If a float, return True, else return False

    Parameters
    ----------
    string : str
        String to check

    Returns
    -------
    bool
       True if input is float, else False
    """
    try:
        int(string)
    except ValueError:
        try:
            float(string)
        except ValueError:
            return False
        else:
            return True
    else:
        return False


def is_string_int(string):
    """
    Check if input string is int. If int, return True, else return False

    Parameters
    ----------
    string : str
        String to check

    Returns
    -------
    bool
       True if input is integer, else False

    """
    try:
        int(string)
    except ValueError:
        return False
    else:
        return True


def print_dict(d, fout=None):
    """
    Print dict d to fout (open file handle)

    Parameters
    ----------
    d : dict
        Dictionary to print
    fout : 
        File handle, can be 'sys.stdout'
    """
    if not fout:
        fout = sys.stdout

    for key in d.keys():
        fout.write(f'{key:15}:: {d[key]}\n')
