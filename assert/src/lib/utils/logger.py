#!/usr/bin/env python

"""
  Utility functions for logging.

    - logger_setup
"""

import logging
import verboselogs

from logging import Logger


def logger_setup(filename: str,
                 log_format: str = "[%(levelname)s] (%(name)s) "
                                   "<%(filename)s:%(lineno)s> "
                                   "%(message)s",
                 level: int = logging.WARNING,
                 file_handler: bool = False,
                 file_format: str = None,
                 file_level: int = None,
                 stream_handler: bool = True,
                 stream_format: str = "[%(levelname)s] :: %(message)s",
                 stream_level: int = None) -> Logger:
    """
    Sets up the logger for the given file

    Parameters
    ----------
    filename :  str
        Name of file
    log_format : str
        Desired format for logs generally
    level : int
        Threshold level for logs generally

    file_handler : bool
        True means logs will be stored in file named '<filename>.log'
    file_format : str
        Desired format for file logs
    file_level : int
        Threshold level for file logs

    stream_handler : bool
        True means that logs will also be outputted in the command-line
    stream_format : str
        Desired format for stream logs
    stream_level : int
        Threshold level for stream logs


    Returns
    -------
    Logger
        logger object that will be used

    """
    # Makes VerboseLogger the default logger class
    verboselogs.install()

    # extract the file name without the extension
    logger_name = filename

    # Formatting
    formatter = logging.Formatter(log_format)

    # Adding the log object
    logger = logging.getLogger(logger_name)

    # Setting the threshold level iff. no handlers are involved
    if not stream_handler and not file_handler:
        logger.setLevel(level)

    # File handler setup
    if file_handler:
        file_handle = logging.FileHandler(
            filename='assert.log',
            # str(Path.cwd()) + '/assert.log',
            mode='a'
        )

        # File handler format
        if file_format:
            file_formatter = logging.Formatter(file_format)
            file_handle.setFormatter(file_formatter)
        else:
            file_handle.setFormatter(formatter)

        # File handler threshold level
        if file_level:
            file_handle.setLevel(file_level)
        else:
            file_handle.setLevel(level)

        logger.addHandler(file_handle)

    # Stream handler setup
    if stream_handler:
        stream_handle = logging.StreamHandler()

        # Stream handler format
        if stream_format:
            stream_formatter = logging.Formatter(stream_format)
            stream_handle.setFormatter(stream_formatter)
        else:
            stream_handle.setFormatter(formatter)

        # Stream handler threshold level
        if stream_level:
            stream_handle.setLevel(stream_level)
        else:
            stream_handle.setLevel(level)

        logger.addHandler(stream_handle)

    # Prevent duplicate messaging
    logger.propagate = False

    return logger
