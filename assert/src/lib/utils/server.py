"""
Server-related functionalities

Functions:
    - get_hostname()
    - is_valid_url()
"""

import os


def get_hostname() -> str:
    """
    Return the hostname (DISCOVER, PLEIADES)

    Returns
    -------
    str
        the host name

    """

    node = os.uname()[1]
    if node[0:8] == 'discover' or node[0:4] == 'borg':
        host = 'DISCOVER'
    elif (node[0:3] == 'pfe' or node[0:4] == 'maia' or
          (node[0] == 'r' and node[4] == 'i') or
          (node[0] == 'r' and node[4] == 'c')):
        host = 'PLEIADES'
    else:
        host = 'DESKTOP'
        # logger.error('could not get host name from node [%s]' % node)

    return host


def is_valid_url(url: str) -> bool:
    import requests

    # Disabling/filtering requests module's loggers
    import logging
    logging.getLogger('requests').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)

    response = requests.get(url)

    return response.status_code == 200
