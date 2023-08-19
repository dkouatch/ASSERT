"""
NU-WRF Testcase Manager

"""
import logging

from src.lib.utils.logger import logger_setup
# from src.lib.utils.paths import create_dir
from src.lib.earthsystems_testcase import EarthSystemsTestcase

logger = logger_setup(filename=__name__,
                      file_handler=True,
                      stream_handler=False,
                      level=logging.INFO)


class NuWrfTestcase(EarthSystemsTestcase):
    def __init__(self, test_cfg: list[dict], scratch_dir: str):
        """
        Parameters
        ----------
        test_cfg : List[dict]
            Information from the test configurations
        scratch_dir: str
            Scratch directory for the model

        """
        super().__init__(test_cfg, scratch_dir)

    def setup_tests(self, time_stamp: str = None) -> None:
        """
        Set up the directory structure for the tests

        Parameters
        ----------
        time_stamp : str
            Time stamp as a string (datetime)

        """
        pass
