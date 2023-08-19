"""
Class to manipulate the test configuration information
from Earth-systems model configuration files

"""
import logging

from typing import List
from src.lib.utils.paths import clean_dir
from src.lib.utils.logger import logger_setup

logger = logger_setup(filename=__name__,
                      file_handler=True,
                      file_level=logging.INFO,
                      stream_handler=False)


class EarthSystemsTestcase:
    def __init__(self, test_cfg: List[dict], scratch_dir: str):
        """
        Parameters
        ----------
        test_cfg : List[dict]
            Information from the test configurations
        scratch_dir: str
            Scratch directory for the model

        """
        # testcases = [{'name': 'H20', 'compilers': 'intel', ...}, ...]
        self.testcases: List[dict] = test_cfg

        # Same structure as testcases but each testcase has flag:
        # {..., run: True, ...}
        self.runnable: List[dict] = list()

        # Dictionary of runnable test names and their respective
        # group of checkpoint directories paths
        # eg. {'H20':
        #          ['.../H20/intel-mpi/', '.../H20/intel-serial/'],
        #      ...}
        self.dirs: dict[str, list[str]] = dict()

        # Scratch directory
        self.scratch_dir = scratch_dir

    def set_runnable_tests(self) -> None:
        """
        Find and store runnable tests by searching for run flag

        """
        for exp in self.testcases:
            try:
                flag = exp['run']
            except KeyError:
                pass
            else:
                if flag:
                    self.runnable.append(exp)
        logger.debug('Runnable tests configured')

    def __print_testcases_info__(self) -> None:
        """
        Print the testcases information.

        """
        for testcase in self.testcases:
            for key in testcase:
                print(f"{key:>15} --> {testcase[key]}")

    def __print_runnable_info__(self) -> None:
        """
        Print the runnable test information

        """
        for runtest in self.runnable:
            for key in runtest:
                print(f"{key:>15} --> {runtest[key]}")

    def get_testcase_names(self) -> list[str]:
        """
        Get the names of all the testcases

        """
        names = list()
        for testcase in self.testcases:
            names.append(testcase['name'])

        return names

    def get_runnable_names(self) -> list[str]:
        """
        Get the names of all the runnable testcases

        """
        names = list()
        for testcase in self.runnable:
            names.append(testcase['name'])

        return names

    def get_testcases(self) -> list[dict]:
        """
        Retrieves list of testcases

        """
        return self.testcases

    def get_runnable(self) -> list[dict]:
        """
        Retrieves list of testcases that will be run

        """
        return self.runnable

    def get_dirs(self) -> dict[str, list[str]]:
        """
        Retrieves dictionary association of testnames and directories

        """
        if self.dirs:
            return self.dirs
        else:
            logger.warning('Test-directory dictionary not yet '
                           'instantiated. Run setup_tests() first.')
            return self.dirs

    def setup_tests(self, time_stamp: str = None) -> None:
        """
        Set up the directory structure for the tests

        Implemented by child classes (model-dependent).

        Parameters
        ----------
        time_stamp : str
            Time stamp as a string (datetime)

        """
        logger.info('ESM — Setting up tests...')

    def clear_test(self, test_name: str) -> None:
        """
        Clears a test's associated directories

        """
        logger.debug(f'ESM — Clearing {test_name}')
        for directory in self.dirs[test_name]:
            clean_dir(directory)


"""
Running test cases dependent on success/failure of builds

Test case dependent on the success/failure of another test case
"""
