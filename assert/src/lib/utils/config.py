#!/usr/bin/env python

"""
Collection of functions to obtain and manipulate the content
of a YAML configuration file.

     - get_config_yaml
     - config_section_map
     - show_yaml_config
     - get_yaml_variable_value
"""

# import re
import logging
import yaml

from src.lib.utils.logger import logger_setup
from src.lib.utils.paths import check_file_exists

from pathlib import Path
from typing import Any

# Logger init
logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.ERROR,
                      stream_handler=False)


def get_yaml_dict(yaml_file_name: str) -> dict:
    """
    Read the YAML configuration text file and return a dictionary object
    containing the different sections of the file.

    Parameters
    ----------
    yaml_file_name : str
         YAML configuration text file

    Returns
    -------
    yaml_dict: dict
        dictionary object of YAML file contents
    """

    check_file_exists(yaml_file_name)

    with open(yaml_file_name, "r") as yaml_file:
        yaml_dict = yaml.safe_load(yaml_file)
        # yamldict = yaml.load(yamldoc, yaml.Loader)

    logger.debug(f'Done reading {yaml_file_name}')

    return yaml_dict


def config_section_map(config, section: str) -> dict:
    """
      For a given section in the configuration file, return a dictionary
      of keys/values of that section.
      Return a dict (i.e. a key,value pair) from each section in config file

      Parameters
      ----------
      config :  
          config object
      section : str
          section name in the configuration file

      Returns
      -------
      section_dict : dict 
          dictionary of keys and values
    """
    section_dict = {}
    options = config.options(section)

    for option in options:
        try:
            section_dict[option] = config.get(section, option)
            if section_dict[option] == -1:
                logger.debug(f'Skip option {option}')
        except KeyError:
            logger.error(f'Exception on {option}!', exc_info=True)
            section_dict[option] = None

    return section_dict


def show_yaml_dict_content(yaml_dict: dict) -> None:
    """
    Print all the variables and their values for each section in the
    YAML Python dictionary.

    Parameters
    ----------
    yaml_dict: dict
        Configuration dictionary

    """
    print('Configuration Settings:')
    print()

    for section_name in yaml_dict.keys():
        # match = not re.search("CONFIG", section_name)
        match = True
        if match:
            print(f"{'-' * (14 + len(section_name))}")
            print(f' >>>>> {section_name} <<<<< ')
            print(f"{'-' * (14 + len(section_name))}")
            if isinstance(yaml_dict[section_name], dict):
                for name, value in yaml_dict[section_name].items():
                    print(f' • {name} = {value}')
                print()
            else:
                print(f" • {yaml_dict[section_name]}")
                print()


def show_yaml_file_content(yaml_file_name: str) -> None:
    """
    Print all the variables and their values for each section in the
    YAML configuration file.

    Parameters
    ----------
    yaml_file_name : str
        configuration file name

    """
    yaml_dict = get_yaml_dict(yaml_file_name)
    show_yaml_dict_content(yaml_dict)


def get_yaml_variable_value(yaml_dict: dict,
                            var_name: str,
                            section_name: str = None,
                            default: Any = None) -> Any:
    """
    Get the value of the variable contains in a specific section.

    Parameters
    ----------
    yaml_dict : dict
        YAML configuration dictionary
    section_name : str
        name of the section
    var_name : str
        name of the variable
    default : 
        default value if variable not present

    Returns
    -------
    Any
        If section does not exist, nothing is returned.
        If the section exists but the variable does not or has no value,
            the default value is returned.
        If both the section and variable exists with a value,
            the value is returned

    """
    if section_name:
        try:
            section_dict = yaml_dict[section_name]
        except KeyError as e:
            logging.error(f'{e}: Section does not exist', exc_info=True)
        else:
            if var_name in section_dict.keys():
                return yaml_dict[section_name][var_name]
            else:
                return default
    else:
        if var_name in yaml_dict.keys():
            return yaml_dict[var_name]
        else:
            return default


def get_testcases(yaml_dict: dict,
                  section_name: str = None,
                  ignore: list[str] = None) -> list[dict]:
    """
    Get model testcases from their configuration dictionaries

    Parameters
    ----------
    yaml_dict : dict
        Config dictionary
    section_name : str
        If we know the testcase section name already
    ignore : list[str]
        List of keys to ignore (aren't testcases)

    Returns
    -------
    list[dict]
        List of testcases w/ their configs as dictionaries

    """
    testcases = list()
    # ignore = ['USERCONFIG', 'COMPCONFIG'] for Model-E

    if section_name:
        if section_name in yaml_dict.keys():
            for key in yaml_dict[section_name].keys():
                section_dict = {'name': key}
                section_dict.update(yaml_dict[section_name][key])
                testcases.append(section_dict)
        else:
            return testcases
    elif ignore:
        for section in yaml_dict.keys():
            if section not in ignore:
                for key in yaml_dict[section].keys():
                    section_dict = {'name': key}
                    section_dict.update(yaml_dict[section][key])
                    testcases.append(section_dict)
    else:
        for key in yaml_dict.keys():
            section_dict = {'name': key}
            section_dict.update(yaml_dict[key])
            testcases.append(section_dict)

    return testcases
